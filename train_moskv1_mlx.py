#!/usr/bin/env python3
# ==============================================================================
# C5-REAL EXERGY CERTIFIED — MOSKV-1 APPLE SILICON MLX FINE-TUNING PIPELINE v2.0
# Framework: Apple Silicon MLX (mlx-lm)
# Base Model: mlx-community/Mistral-7B-Instruct-v0.3-4bit
# Data Directory: data_mlx/ (train.jsonl: 27,352 | valid.jsonl: 1,440)
# ==============================================================================

import argparse
import os
import sys
import subprocess
from pathlib import Path

BASE_DIR = Path("/Users/borjafernandezangulo/10_PROJECTS/escohotado-corpus")
DATA_DIR = BASE_DIR / "data_mlx"
DEFAULT_MODEL = "mlx-community/Mistral-7B-Instruct-v0.3-4bit"
DEFAULT_ADAPTER_PATH = BASE_DIR / "moskv1_mlx_adapters"

def parse_args():
    parser = argparse.ArgumentParser(description="MOSKV-1 MLX Fine-Tuning Engine (Apple Silicon Metal)")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="ID o ruta del modelo base MLX")
    parser.add_argument("--data", type=str, default=str(DATA_DIR), help="Ruta al directorio con train.jsonl y valid.jsonl")
    parser.add_argument("--iters", type=int, default=1000, help="Número total de iteraciones de entrenamiento")
    parser.add_argument("--batch-size", type=int, default=2, help="Batch size por iteración de gradiente")
    parser.add_argument("--learning-rate", type=float, default=1e-5, help="Tasa de aprendizaje (Learning Rate)")
    parser.add_argument("--lora-layers", type=int, default=16, help="Número de capas transformadoras a adaptar")
    parser.add_argument("--adapter-path", type=str, default=str(DEFAULT_ADAPTER_PATH), help="Directorio para guardar adaptadores LoRA")
    parser.add_argument("--fuse", action="store_true", help="Fusionar adaptadores con el modelo base al finalizar")
    return parser.parse_args()

def verify_dataset():
    train_p = DATA_DIR / "train.jsonl"
    valid_p = DATA_DIR / "valid.jsonl"
    if not train_p.exists() or not valid_p.exists() or train_p.stat().st_size == 0:
        print("[!] Dataset MLX incompleto o no encontrado. Auto-ejecutando prepare_master_dataset.py...")
        subprocess.run([sys.executable, str(BASE_DIR / "prepare_master_dataset.py")], check=True)

def main():
    args = parse_args()
    print("=== [MOSKV-1 MLX Fine-Tuning Engine v2.0 — Apple Silicon Metal] ===")
    print(f"  ├─ Modelo Base: {args.model}")
    print(f"  ├─ Directorio Datos: {args.data}")
    print(f"  ├─ Iteraciones: {args.iters} | Batch Size: {args.batch_size} | LR: {args.learning_rate}")
    print(f"  └─ Adaptadores LoRA: {args.adapter_path} (Capas: {args.lora_layers})")

    verify_dataset()

    # Verificar si mlx_lm está disponible
    try:
        import mlx_lm
        print("[✓] Runtime `mlx_lm` detectado.")
    except ImportError:
        print("[!] `mlx_lm` no está instalado en el entorno actual de Python.")
        print("    Para instalarlo en macOS Apple Silicon ejecute:")
        print("    pip install mlx-lm")
        sys.exit(1)

    cmd = [
        "python3", "-m", "mlx_lm", "lora",
        "--model", args.model,
        "--data", "data_mlx",
        "--train",
        "--batch-size", "1",
        "--max-seq-length", "2048",
        "--grad-checkpoint",
        "--val-batches", "10",
        "--steps-per-report", "10",
        "--steps-per-eval", "25",
        "--num-layers", str(args.lora_layers),
        "--learning-rate", str(args.learning_rate),
        "--iters", str(args.iters),
        "--adapter-path", args.adapter_path
    ]

    print(f"\n[*] Lanzando comando de entrenamiento LoRA...")
    print(f"    $ {' '.join(cmd)}\n")

    try:
        subprocess.run(cmd, check=True)
        print(f"\n[✓] Entrenamiento MLX completado exitosamente.")
        print(f"    Adaptadores guardados en: {args.adapter_path}")

        if args.fuse:
            print("\n[*] Fusionando adaptadores LoRA con modelo base (mlx_lm.fuse)...")
            fused_path = str(BASE_DIR / "moskv1_fused_model")
            fuse_cmd = [
                sys.executable, "-m", "mlx_lm.fuse",
                "--model", args.model,
                "--adapter-path", args.adapter_path,
                "--save-path", fused_path
            ]
            subprocess.run(fuse_cmd, check=True)
            print(f"[✓] Modelo fusionado exitosamente en: {fused_path}")

    except subprocess.CalledProcessError as e:
        print(f"\n[!] Error durante la ejecución de entrenamiento MLX: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
