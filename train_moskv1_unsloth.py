#!/usr/bin/env python3
# ==============================================================================
# C5-REAL EXERGY CERTIFIED — MOSKV-1 UN SLOTH / CUDA FINE-TUNING PIPELINE v2.0
# Base Models Supported: Mistral-7B-Instruct-v0.3, Qwen2.5-7B-Instruct, LLaMA-3.1-8B
# Dataset: 28.792 Muestras ShareGPT (moskv1_28792_master_sharegpt.jsonl)
# Invariante Ω118 / Ξ = 23.000
# ==============================================================================

import argparse
import os
import sys
import torch

def parse_args():
    parser = argparse.ArgumentParser(description="MOSKV-1 Unsloth / CUDA Fine-Tuning Engine")
    parser.add_argument(
        "--model-name",
        type=str,
        default="unsloth/Mistral-7B-Instruct-v0.3-bnb-4bit",
        help="ID del modelo base de Unsloth (ej. unsloth/Qwen2.5-7B-Instruct-bnb-4bit, unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit)"
    )
    parser.add_argument("--dataset-path", type=str, default="moskv1_28792_master_sharegpt.jsonl", help="Ruta al dataset maestro ShareGPT")
    parser.add_argument("--output-dir", type=str, default="moskv1_dora_adapter", help="Directorio de salida para los adaptadores DoRA")
    parser.add_argument("--max-seq-length", type=int, default=4096, help="Ventana de contexto máxima en tokens")
    parser.add_argument("--epochs", type=int, default=1, help="Número de épocas de entrenamiento")
    parser.add_argument("--batch-size", type=int, default=4, help="Batch size por GPU")
    parser.add_argument("--grad-accum", type=int, default=4, help="Pasos de acumulación de gradiente")
    parser.add_argument("--learning-rate", type=float, default=2e-4, help="Tasa de aprendizaje (Learning Rate)")
    parser.add_argument("--lora-rank", type=int, default=16, help="Rango (Rank r) de DoRA")
    parser.add_argument("--lora-alpha", type=int, default=32, help="Alpha de DoRA")
    parser.add_argument("--export-gguf", type=str, default="q4_k_m", choices=["none", "q4_k_m", "q5_k_m", "q8_0"], help="Método de cuantización GGUF a exportar")
    return parser.parse_args()

def main():
    args = parse_args()
    print("=== [MOSKV-1 Fine-Tuning Engine v2.0 — CUDA / Unsloth] ===")
    print(f"  ├─ Modelo Base: {args.model_name}")
    print(f"  ├─ Dataset: {args.dataset_path}")
    print(f"  ├─ Ventana Contexto: {args.max_seq_length} tokens | Épocas: {args.epochs}")
    print(f"  ├─ DoRA Rank: {args.lora_rank} | Alpha: {args.lora_alpha} | LR: {args.learning_rate}")
    print(f"  └─ Exportación GGUF: {args.export_gguf}")

    try:
        from unsloth import FastLanguageModel
        from unsloth.chat_templates import get_chat_template
        from datasets import load_dataset
        from trl import SFTTrainer
        from transformers import TrainingArguments
    except ImportError:
        print("[!] Unsloth no está instalado localmente. Este script debe ejecutarse en un entorno GPU CUDA")
        print("    (NVIDIA Colab T4/A100/H100, RunPod, Modal, o Servidor Linux con CUDA).")
        print("    Para entrenamiento local en macOS Apple Silicon, utilice `train_moskv1_mlx.py`.")
        sys.exit(1)

    if not os.path.exists(args.dataset_path):
        print(f"[!] {args.dataset_path} no encontrado. Ejecutando preparador de dataset...")
        os.system(f"{sys.executable} prepare_master_dataset.py")

    print(f"[*] Cargando modelo base cuantizado: {args.model_name}...")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = args.model_name,
        max_seq_length = args.max_seq_length,
        dtype = None,
        load_in_4bit = True,
    )

    print(f"[*] Inyectando adaptadores DoRA (r={args.lora_rank}, alpha={args.lora_alpha})...")
    model = FastLanguageModel.get_peft_model(
        model,
        r = args.lora_rank,
        target_modules = [
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj"
        ],
        lora_alpha = args.lora_alpha,
        lora_dropout = 0,
        bias = "none",
        use_gradient_checkpointing = "unsloth",
        random_state = 3407,
        use_rslora = False,
        use_dora = True,
    )

    print("[*] Mapeando plantilla de chat ChatML/ShareGPT...")
    tokenizer = get_chat_template(
        tokenizer,
        chat_template = "chatml",
        mapping = {"role": "role", "content": "content", "user": "user", "assistant": "assistant"}
    )

    def formatting_prompts_func(examples):
        convos = examples["messages"]
        texts = [tokenizer.apply_chat_template(convo, tokenize=False, add_generation_prompt=False) for convo in convos]
        return {"text": texts}

    print(f"[*] Cargando dataset: {args.dataset_path}...")
    dataset = load_dataset("json", data_files=args.dataset_path, split="train")
    dataset = dataset.map(formatting_prompts_func, batched=True)

    print("[*] Configurando SFTTrainer...")
    trainer = SFTTrainer(
        model = model,
        tokenizer = tokenizer,
        train_dataset = dataset,
        dataset_text_field = "text",
        max_seq_length = args.max_seq_length,
        dataset_num_proc = 4,
        packing = False,
        args = TrainingArguments(
            per_device_train_batch_size = args.batch_size,
            gradient_accumulation_steps = args.grad_accum,
            warmup_ratio = 0.05,
            num_train_epochs = args.epochs,
            learning_rate = args.learning_rate,
            fp16 = not torch.cuda.is_bf16_supported(),
            bf16 = torch.cuda.is_bf16_supported(),
            logging_steps = 10,
            save_strategy = "steps",
            save_steps = 300,
            optim = "adamw_8bit",
            weight_decay = 0.01,
            lr_scheduler_type = "cosine",
            seed = 3407,
            output_dir = "outputs_moskv1",
            report_to = "none",
        ),
    )

    print("[🚀] Lanzando entrenamiento MOSKV-1...")
    trainer.train()

    print(f"[*] Guardando adaptadores DoRA en: {args.output_dir}")
    model.save_pretrained(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)

    if args.export_gguf != "none":
        gguf_filename = f"moskv1_{args.export_gguf}.gguf"
        print(f"[*] Exportando modelo compilado a GGUF ({args.export_gguf}) -> {gguf_filename}...")
        try:
            model.save_pretrained_gguf(gguf_filename, tokenizer, quantization_method=args.export_gguf)
            print(f"[✓] Modelo GGUF generado exitosamente: {gguf_filename}")
        except Exception as e:
            print(f"[!] Advertencia al exportar GGUF: {e}")

    print("\n[✓] MOSKV-1 (Unsloth DoRA) cristalizado exitosamente.")

if __name__ == "__main__":
    main()
