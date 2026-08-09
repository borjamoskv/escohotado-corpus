#!/usr/bin/env python3
# ==============================================================================
# C5-REAL EXERGY CERTIFIED — MOSKV-1 APPLE SILICON MLX FINE-TUNING PIPELINE
# Framework: Apple Silicon MLX (mlx-lm)
# Base Model: mlx-community/Mistral-7B-Instruct-v0.3-4bit
# Dataset: 28.792 Muestras ShareGPT (moskv1_28792_master_sharegpt.jsonl)
# ==============================================================================

import os
import sys
import subprocess

def main():
    print("=== [MOSKV-1 MLX Fine-Tuning Engine — Apple Silicon Metal] ===")
    
    dataset_file = "moskv1_28792_master_sharegpt.jsonl"
    if not os.path.exists(dataset_file):
        print(f"[!] {dataset_file} no existe. Generándolo...")
        subprocess.run([sys.executable, "prepare_master_dataset.py"], check=True)

    # Verificar si mlx_lm está disponible
    try:
        import mlx_lm
    except ImportError:
        print("[!] mlx_lm no está instalado en este entorno de Python.")
        print("    Para instalarlo en macOS Apple Silicon execute: pip install mlx-lm")
        sys.exit(1)

    model_id = "mlx-community/Mistral-7B-Instruct-v0.3-4bit"
    adapter_path = "moskv1_mlx_adapters"

    print(f"[*] Lanzando fine-tuning LoRA en Apple Silicon (Metal MPS)...")
    cmd = [
        "python3", "-m", "mlx_lm.lora",
        "--model", model_id,
        "--data", ".",
        "--train",
        "--batch-size", "2",
        "--lora-layers", "16",
        "--learning-rate", "1e-5",
        "--iters", "1000",
        "--adapter-path", adapter_path
    ]
    
    print(f"[*] Comando: {' '.join(cmd)}")
    subprocess.run(cmd)

if __name__ == "__main__":
    main()
