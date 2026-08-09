#!/usr/bin/env python3
# C5-REAL EXERGY CERTIFIED
# Script de Entrenamiento PEFT/DoRA mediante Unsloth
# Invariante Ω118 - Corpus Escohotado (Máxima Exergía)

import os
import torch
from unsloth import FastLanguageModel
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments
from unsloth.chat_templates import get_chat_template

# ==========================================
# 1. Configuración de Exergía (Hardware)
# ==========================================
max_seq_length = 2048 # Soporte RoPE scaling interno
dtype = None          # Auto-detección (Float16/Bfloat16)
load_in_4bit = True   # Cuantización de cero anergía (QLoRA)

model_name = "unsloth/Meta-Llama-3-8B-Instruct-bnb-4bit"
dataset_path = "moskv1_filosofo_sharegpt.jsonl"
output_dir = "lora_model_escohotado_omega118"

print("[*] Inicializando modelo base con Unsloth (4-bit)...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = model_name,
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
)

# ==========================================
# 2. Inyección de Adaptadores DoRA
# ==========================================
print("[*] Inyectando adaptadores DoRA (Rank=16, Alpha=32)...")
model = FastLanguageModel.get_peft_model(
    model,
    r = 16,
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj",],
    lora_alpha = 32,
    lora_dropout = 0,      # Dropout = 0 para máxima eficiencia
    bias = "none",
    use_gradient_checkpointing = "unsloth", # O(1) VRAM exergy
    random_state = 3407,
    use_rslora = False,
    use_dora = True,       # DoRA activado (Mejor rendimiento que LoRA estándar)
)

# ==========================================
# 3. Mapeo del Dataset ShareGPT/ChatML
# ==========================================
print(f"[*] Cargando corpus epistémico: {dataset_path}")
tokenizer = get_chat_template(
    tokenizer,
    chat_template = "chatml", # Formato emitido por el Swarm Miner
    mapping = {"role" : "role", "content" : "content", "user" : "user", "assistant" : "assistant"}
)

def formatting_prompts_func(examples):
    convos = examples["messages"]
    texts = [tokenizer.apply_chat_template(convo, tokenize=False, add_generation_prompt=False) for convo in convos]
    return {"text": texts}

dataset = load_dataset("json", data_files=dataset_path, split="train")
dataset = dataset.map(formatting_prompts_func, batched=True)

# ==========================================
# 4. Orquestación del Entrenamiento
# ==========================================
print("[*] Configurando SFTTrainer (Supervised Fine-Tuning)...")
trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = max_seq_length,
    dataset_num_proc = 2,
    packing = False, # Soporte para secuencias variables
    args = TrainingArguments(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        warmup_steps = 5,
        max_steps = 60, # Ajustable según convergencia (1 epoch recomendada)
        learning_rate = 2e-4,
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 1,
        optim = "adamw_8bit",
        weight_decay = 0.01,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "outputs",
    ),
)

# ==========================================
# 5. Colapso Final: Ejecución
# ==========================================
print("[*] Iniciando entrenamiento...")
trainer_stats = trainer.train()

print(f"[*] Entrenamiento finalizado. Guardando adaptadores DoRA en {output_dir}...")
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)

print("[*] ¡Proceso completado! El modelo está listo para inferencia determinista bajo el Invariante Ω118.")
