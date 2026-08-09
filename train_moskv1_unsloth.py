#!/usr/bin/env python3
# ==============================================================================
# C5-REAL EXERGY CERTIFIED — MOSKV-1 MISTRAL FINE-TUNING PIPELINE
# Base Model: Mistral-7B-Instruct-v0.3 (Unsloth DoRA 4-bit)
# Dataset: 28.792 Muestras ShareGPT (Multi-Dominio: Ing, Fis, Med, Mus, Abg)
# Invariante Ω118 / Ξ = 23.000
# ==============================================================================

import os
import sys
import torch
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments

try:
    from unsloth import FastLanguageModel
    from unsloth.chat_templates import get_chat_template
except ImportError:
    print("[!] Unsloth no está instalado localmente. Este script está diseñado para ejecutarse en entornos GPU CUDA")
    print("    (NVIDIA Colab T4/A100/H100, RunPod, Modal, o Servidor Linux CUDA).")
    print("    Para entrenamiento local en Apple Silicon, utilice `train_moskv1_mlx.py`.")

def main():
    print("=== [MOSKV-1 Fine-Tuning Engine — Base: Mistral-7B-Instruct-v0.3] ===")
    
    # --------------------------------------------------------------------------
    # 1. Configuración de Hardware y Ventana de Atención
    # --------------------------------------------------------------------------
    max_seq_length = 4096  # Ventana de contexto amplia para análisis sistémico
    dtype = None           # Auto-detecta Float16 o Bfloat16 según GPU
    load_in_4bit = True    # Cuantización de 4 bits para ahorro extremo de VRAM (QLoRA)
    
    model_name = "unsloth/Mistral-7B-Instruct-v0.3-bnb-4bit"
    dataset_path = "moskv1_28792_master_sharegpt.jsonl"
    output_dir = "moskv1_mistral_7b_dora_adapter"

    if not os.path.exists(dataset_path):
        print(f"[!] No se encontró {dataset_path}. Ejecutando auto-reparación preparatoria...")
        os.system("python3 prepare_master_dataset.py")

    print(f"[*] Cargando modelo base: {model_name}...")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name = model_name,
        max_seq_length = max_seq_length,
        dtype = dtype,
        load_in_4bit = load_in_4bit,
    )

    # --------------------------------------------------------------------------
    # 2. Inyección de Adaptadores DoRA (Weight Decomposed Low-Rank Adaptation)
    # --------------------------------------------------------------------------
    print("[*] Inyectando adaptadores DoRA (Rank=16, Alpha=32, target=all-linear)...")
    model = FastLanguageModel.get_peft_model(
        model,
        r = 16,
        target_modules = [
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj"
        ],
        lora_alpha = 32,
        lora_dropout = 0,                       # Dropout=0 para máxima exergía y velocidad
        bias = "none",
        use_gradient_checkpointing = "unsloth", # Memoria VRAM O(1)
        random_state = 3407,
        use_rslora = False,
        use_dora = True,                        # DoRA activado (Mejor convergencia que LoRA estándar)
    )

    # --------------------------------------------------------------------------
    # 3. Formateo ShareGPT / ChatML
    # --------------------------------------------------------------------------
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

    print(f"[*] Ingestando dataset epistémico maestro ({dataset_path})...")
    dataset = load_dataset("json", data_files=dataset_path, split="train")
    dataset = dataset.map(formatting_prompts_func, batched=True)

    # --------------------------------------------------------------------------
    # 4. Orquestación del Entrenamiento (SFTTrainer)
    # --------------------------------------------------------------------------
    print("[*] Configurando SFTTrainer...")
    trainer = SFTTrainer(
        model = model,
        tokenizer = tokenizer,
        train_dataset = dataset,
        dataset_text_field = "text",
        max_seq_length = max_seq_length,
        dataset_num_proc = 4,
        packing = False,
        args = TrainingArguments(
            per_device_train_batch_size = 4,
            gradient_accumulation_steps = 4,   # Effective Batch Size = 16
            warmup_ratio = 0.05,
            num_train_epochs = 1,              # 1 época sobre 28.792 muestras (~1.800 pasos)
            learning_rate = 2e-4,
            fp16 = not torch.cuda.is_bf16_supported(),
            bf16 = torch.cuda.is_bf16_supported(),
            logging_steps = 10,
            save_strategy = "steps",
            save_steps = 300,
            optim = "adamw_8bit",
            weight_decay = 0.01,
            lr_scheduler_type = "cosine",
            seed = 3407,
            output_dir = "outputs_moskv1_mistral",
            report_to = "none",
        ),
    )

    # --------------------------------------------------------------------------
    # 5. Ejecución del Fine-Tuning
    # --------------------------------------------------------------------------
    print("[🚀] Iniciando entrenamiento MOSKV-1...")
    trainer_stats = trainer.train()

    print(f"[*] Fine-Tuning completado. Guardando adaptadores DoRA en: {output_dir}")
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)

    # --------------------------------------------------------------------------
    # 6. Exportación a Formato GGUF (Para inferencia local con Ollama / llama.cpp)
    # --------------------------------------------------------------------------
    print("[*] Exportando modelo compilado a GGUF (Q4_K_M)...")
    try:
        model.save_pretrained_gguf("moskv1_mistral_7b_q4_k_m.gguf", tokenizer, quantization_method="q4_k_m")
        print("[✓] Modelo exportado a GGUF exitosamente: moskv1_mistral_7b_q4_k_m.gguf")
    except Exception as e:
        print(f"[!] Exportación GGUF omitida/advertencia: {e}")

    print("\n[✓] MOSKV-1 (Mistral-7B DoRA) cristalizado y listo para despliegue.")

if __name__ == "__main__":
    main()
