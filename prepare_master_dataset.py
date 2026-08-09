#!/usr/bin/env python3
"""
MOSKV-1 Dataset Preparator (C5-REAL Master Integrator)
Funde y valida las 28.792 muestras limpias en formato ShareGPT distribuidas en los 5 dominios epistémicos:
- Ingeniero: 21.581
- Físico: 2.580
- Médico: 2.388
- Músico: 2.123
- Abogado: 120
TOTAL: 28.792
"""

import json
import os
import random
from pathlib import Path

# Semilla fija para reproducibilidad determinista (Invariante C5-REAL)
SEED = 3407
random.seed(SEED)

SOURCE_DIR = Path("/Users/borjafernandezangulo/10_PROJECTS/20_VAULT/wa-nexus/lora_swarm_ultimate_output")
OUTPUT_FILE = Path("/Users/borjafernandezangulo/10_PROJECTS/escohotado-corpus/moskv1_28792_master_sharegpt.jsonl")

DOMAIN_FILES = [
    "moskv1_ingeniero_sharegpt.jsonl",
    "moskv1_fisico_sharegpt.jsonl",
    "moskv1_medico_sharegpt.jsonl",
    "moskv1_musico_sharegpt.jsonl",
    "moskv1_abogado_sharegpt.jsonl",
]

def main():
    print("=== [MOSKV-1 Master Dataset Integrator] ===")
    total_samples = 0
    domain_counts = {}
    master_records = []

    for fname in DOMAIN_FILES:
        fpath = SOURCE_DIR / fname
        if not fpath.exists():
            print(f"[!] Error: No se encontró el archivo {fpath}")
            continue

        count = 0
        with open(fpath, "r", encoding="utf-8") as f:
            for line_idx, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    if "messages" not in data or not isinstance(data["messages"], list):
                        print(f"[!] Warning: Estructura inválida en {fname}:{line_idx}")
                        continue
                    master_records.append(data)
                    count += 1
                except json.JSONDecodeError as e:
                    print(f"[!] Error JSON en {fname}:{line_idx} -> {e}")

        domain_counts[fname] = count
        total_samples += count
        print(f"  └─ {fname}: {count} muestras integradas.")

    print(f"\n[*] Total de muestras recolectadas: {total_samples}")

    # Barajado determinista para balancear gradientes entre dominios durante fine-tuning
    print(f"[*] Barajando dataset deterministamente (seed={SEED})...")
    random.shuffle(master_records)

    print(f"[*] Escribiendo dataset maestro en: {OUTPUT_FILE}")
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out_f:
        for record in master_records:
            out_f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"[✓] Integración exitosa. Archivo listo con exactamente {len(master_records)} muestras.")

if __name__ == "__main__":
    main()
