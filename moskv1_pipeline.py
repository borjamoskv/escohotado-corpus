#!/usr/bin/env python3
# ==============================================================================
# MOSKV-1 UNIFIED AGENTIC PIPELINE ORCHESTRATOR v2.0 (C5-REAL Certified)
# Control central para dataset, entrenamiento (MLX / Unsloth), e inferencia
# ==============================================================================

import argparse
import json
import os
import sys
import subprocess
from pathlib import Path

BASE_DIR = Path("/Users/borjafernandezangulo/10_PROJECTS/escohotado-corpus")

def cmd_prepare(args):
    print("=== [MOSKV-1 Pipeline: Preparación & Sanitización de Datasets] ===")
    script = BASE_DIR / "prepare_master_dataset.py"
    subprocess.run([sys.executable, str(script)], check=True)

def cmd_train_mlx(args):
    print("=== [MOSKV-1 Pipeline: Entrenamiento Local en Apple Silicon (Metal MLX)] ===")
    script = BASE_DIR / "train_moskv1_mlx.py"
    cmd = [sys.executable, str(script), "--model", args.model, "--iters", str(args.iters), "--batch-size", str(args.batch_size)]
    if args.fuse:
        cmd.append("--fuse")
    subprocess.run(cmd, check=True)

def cmd_train_unsloth(args):
    print("=== [MOSKV-1 Pipeline: Entrenamiento CUDA / Unsloth (Nube / RunPod / Colab)] ===")
    script = BASE_DIR / "train_moskv1_unsloth.py"
    print(f"[*] Para ejecutar en GPU CUDA (Linux/RunPod/Colab):")
    print(f"    python3 {script.name} --model-name {args.model_name} --epochs {args.epochs} --export-gguf {args.export_gguf}")

def cmd_evaluate(args):
    print("=== [MOSKV-1 Pipeline: Evaluación Multi-Dominio & Léxico] ===")
    script = BASE_DIR / "infer_moskv1.py"
    cmd = [sys.executable, str(script)]
    if args.model:
        cmd.extend(["--model", args.model])
    if args.adapter_path:
        cmd.extend(["--adapter-path", args.adapter_path])
    if args.dry_run:
        cmd.append("--dry-run")
    subprocess.run(cmd, check=True)

def cmd_status(args):
    print("=== [MOSKV-1 Pipeline: Estado del Sistema & Salud de Artefactos] ===")
    
    master_ds = BASE_DIR / "moskv1_28792_master_sharegpt.jsonl"
    mlx_train = BASE_DIR / "data_mlx" / "train.jsonl"
    mlx_valid = BASE_DIR / "data_mlx" / "valid.jsonl"
    report_f = BASE_DIR / "dataset_health_report.json"
    adapters_f = BASE_DIR / "moskv1_mlx_adapters"
    fused_f = BASE_DIR / "moskv1_fused_model"

    def fmt_size(p: Path):
        if not p.exists():
            return "No existe"
        if p.is_dir():
            count = len(list(p.glob("*")))
            return f"Directorio ({count} archivos)"
        return f"{p.stat().st_size / (1024*1024):.2f} MB"

    print(f"  ├─ Dataset Maestro ShareGPT : {master_ds} [{fmt_size(master_ds)}]")
    print(f"  ├─ Split MLX Train (95%)    : {mlx_train} [{fmt_size(mlx_train)}]")
    print(f"  ├─ Split MLX Valid (5%)     : {mlx_valid} [{fmt_size(mlx_valid)}]")
    print(f"  ├─ Adaptadores LoRA MLX     : {adapters_f} [{fmt_size(adapters_f)}]")
    print(f"  ├─ Modelo Fused MLX         : {fused_f} [{fmt_size(fused_f)}]")

    if report_f.exists():
        print(f"\n--- REPORTE DE SALUD DEL DATASET ({report_f.name}) ---")
        try:
            with open(report_f, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"  ├─ Estado: {data.get('status')}")
            print(f"  ├─ Muestras Únicas: {data.get('total_unique_samples'):,}")
            print(f"  ├─ Duplicados Purgados: {data.get('total_duplicates_purged'):,}")
            print(f"  └─ Tokens Estimados: ~{data.get('total_estimated_tokens'):,} tokens")
        except Exception as e:
            print(f"  [!] Error leyendo reporte: {e}")

def main():
    parser = argparse.ArgumentParser(description="MOSKV-1 Unified Pipeline Orchestrator")
    subparsers = parser.add_subparsers(dest="subcommand", help="Subcomandos del pipeline")

    # Command: prepare
    p_prep = subparsers.add_parser("prepare", help="Funde, deduplica y prepara datasets")
    p_prep.set_defaults(func=cmd_prepare)

    # Command: train-mlx
    p_mlx = subparsers.add_parser("train-mlx", help="Lanza entrenamiento local en Apple Silicon (Metal MLX)")
    p_mlx.add_argument("--model", type=str, default="mlx-community/Mistral-7B-Instruct-v0.3-4bit")
    p_mlx.add_argument("--iters", type=int, default=1000)
    p_mlx.add_argument("--batch-size", type=int, default=2)
    p_mlx.add_argument("--fuse", action="store_true")
    p_mlx.set_defaults(func=cmd_train_mlx)

    # Command: train-unsloth
    p_unsloth = subparsers.add_parser("train-unsloth", help="Genera comando para entrenamiento CUDA / Unsloth")
    p_unsloth.add_argument("--model-name", type=str, default="unsloth/Mistral-7B-Instruct-v0.3-bnb-4bit")
    p_unsloth.add_argument("--epochs", type=int, default=1)
    p_unsloth.add_argument("--export-gguf", type=str, default="q4_k_m")
    p_unsloth.set_defaults(func=cmd_train_unsloth)

    # Command: evaluate
    p_eval = subparsers.add_parser("evaluate", help="Ejecuta benchmark de inferencia multi-dominio")
    p_eval.add_argument("--model", type=str, default=None)
    p_eval.add_argument("--adapter-path", type=str, default=None)
    p_eval.add_argument("--dry-run", action="store_true")
    p_eval.set_defaults(func=cmd_evaluate)

    # Command: status
    p_stat = subparsers.add_parser("status", help="Muestra el estado del sistema y salud del dataset")
    p_stat.set_defaults(func=cmd_status)

    args = parser.parse_args()
    if not args.subcommand:
        parser.print_help()
        sys.exit(1)

    args.func(args)

if __name__ == "__main__":
    main()
