#!/usr/bin/env python3
# ==============================================================================
# C5-REAL EXERGY CERTIFIED — MOSKV-1 APPLE SILICON MLX FINE-TUNING PIPELINE v2.0
# Framework: Apple Silicon MLX (mlx-lm)
# Base Model: mlx-community/Mistral-7B-Instruct-v0.3-4bit
# Data Directory: data_mlx/ (train.jsonl: 27,352 | valid.jsonl: 1,440)
# ==============================================================================

import argparse
import sys
import subprocess
from pathlib import Path
from corpus_quality import audit

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data_mlx"
DEFAULT_MODEL = "mlx-community/Mistral-7B-Instruct-v0.3-4bit"
DEFAULT_ADAPTER_PATH = BASE_DIR / "moskv1_mlx_adapters"

def parse_args():
    parser = argparse.ArgumentParser(description="MOSKV-1 MLX Fine-Tuning Engine (Apple Silicon Metal)")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="ID o ruta del modelo base MLX")
    parser.add_argument("--data", type=str, default=str(DATA_DIR), help="Ruta al directorio con train.jsonl, valid.jsonl y review.jsonl")
    parser.add_argument("--source-root", type=Path, default=BASE_DIR, help="Root of reviewed evidence files")
    parser.add_argument("--iters", type=int, default=50, help="Número total de iteraciones de entrenamiento")
    parser.add_argument("--batch-size", type=int, default=1, help="Batch size por iteración de gradiente")
    parser.add_argument("--grad-accum", type=int, default=2, help="Pasos de acumulación de gradiente")
    parser.add_argument("--max-seq-length", type=int, default=384, help="Longitud máxima de secuencia en tokens")
    parser.add_argument("--learning-rate", type=float, default=2.5e-5, help="Tasa de aprendizaje (Learning Rate)")
    parser.add_argument("--lora-layers", type=int, default=4, help="Número de capas transformadoras a adaptar")
    parser.add_argument("--adapter-path", type=str, default=str(DEFAULT_ADAPTER_PATH), help="Directorio para guardar adaptadores LoRA")
    parser.add_argument("--resume", action="store_true", help="Reanudar desde adapters.safetensors existentes en adapter-path")
    parser.add_argument("--fuse", action="store_true", help="Fusionar adaptadores con el modelo base al finalizar")
    return parser.parse_args()

def verify_dataset(data_dir, source_root):
    """Refuse training on unreviewed or contaminated data; never rebuild silently."""
    report = audit(Path(data_dir), source_root)
    if not report["gate_passed"]:
        print("[!] Dataset quality gate failed: " + ", ".join(report["gate_failures"]), file=sys.stderr)
        print("Run corpus_quality.py --data <directory> --gate for details.", file=sys.stderr)
        raise SystemExit(1)


def main():
    args = parse_args()
    print("=== [MOSKV-1 MLX Fine-Tuning Engine v2.0 — Apple Silicon Metal] ===")
    print(f"  ├─ Modelo Base: {args.model}")
    print(f"  ├─ Directorio Datos: {args.data}")
    print(f"  ├─ Iteraciones: {args.iters} | Batch Size: {args.batch_size} (Accum: {args.grad_accum}) | LR: {args.learning_rate}")
    print(f"  └─ Adaptadores LoRA: {args.adapter_path} (Capas: {args.lora_layers} | MaxSeq: {args.max_seq_length})")

    verify_dataset(args.data, args.source_root)

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
        sys.executable, "-m", "mlx_lm", "lora",
        "--model", args.model,
        "--data", str(args.data),
        "--train",
        "--batch-size", str(args.batch_size),
        "--grad-accumulation-steps", str(args.grad_accum),
        "--max-seq-length", str(args.max_seq_length),
        "--grad-checkpoint",
        "--mask-prompt",
        "--val-batches", "1",
        "--steps-per-report", "5",
        "--steps-per-eval", "500",
        "--num-layers", str(args.lora_layers),
        "--learning-rate", str(args.learning_rate),
        "--iters", str(args.iters),
        "--save-every", str(args.iters),
        "--adapter-path", str(args.adapter_path)
    ]

    if args.resume:
        resume_ckpt = str(Path(args.adapter_path) / "adapters.safetensors")
        cmd += ["--resume-adapter-file", resume_ckpt]
        print(f"[*] Reanudando desde checkpoint: {resume_ckpt}")

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
