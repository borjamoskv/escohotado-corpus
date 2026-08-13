#!/usr/bin/env python3
# ==============================================================================
# MOSKV-1 MULTI-DOMAIN TEST BENCH & INFERENCE EVALUATOR v2.0
# Evaluación de inferencia en vivo y auditoría de léxico para los 5 dominios
# (Ingeniero, Físico, Médico, Músico, Abogado)
# ==============================================================================

import argparse
import json
import sys
import time
from pathlib import Path

PROMPTS = [
    {
        "domain": "Ingeniero",
        "system": "Eres Moskv-1 (Modo Ingeniería de Software & C++20/Rust). Invariante: Cero-Anergía y exergía máxima.",
        "user": "Explica la garantía de atómica del Sequencer Lock-Free SPSC y el Invariante CALM II'.",
        "keywords": ["lock-free", "spsc", "atomic", "calm", "ring buffer", "memoria", "exergía"]
    },
    {
        "domain": "Físico",
        "system": "Eres Moskv-1 (Modo Física & Termodinámica). Analizas el sistema mediante mecánica estadística y cotas de Landauer.",
        "user": "¿Cómo afecta el borrado de información de 1 bit al consumo termodinámico mínimo (kT ln 2)?",
        "keywords": ["landauer", "entropía", "kt ln 2", "información", "termodinámica", "disipación"]
    },
    {
        "domain": "Médico",
        "system": "Eres Moskv-1 (Modo Fisiología & Neurociencia). Analizas mediante homeostosis de redes neuronales y bioenergética.",
        "user": "Describe la modulación neurotransmisora de la dopamina en circuitos estriatales.",
        "keywords": ["dopamina", "estriado", "neurotransmisor", "sinapsis", "receptores d1/d2", "circuito"]
    },
    {
        "domain": "Músico",
        "system": "Eres Moskv-1 (Modo Teoría Musical & Acústica Físico-Matemática). Analizas análisis espectral y armónicos.",
        "user": "Analiza la afinación temperada vs justa a través de las proporciones de frecuencia pitagóricas.",
        "keywords": ["frecuencia", "temperada", "pitagórica", "armónicos", "quintas", "acústica"]
    },
    {
        "domain": "Abogado",
        "system": "Eres Moskv-1 (Modo Derecho, Invariantes de Gobernanza & SCITT). Analizas atestaciones jurídicas y no repudio.",
        "user": "¿Cómo valida el registro SCITT la precedencia temporal y la integridad forense de los artefactos?",
        "keywords": ["scitt", "atestación", "merkle", "no repudio", "forense", "gobernanza", "eu ai act"]
    }
]

def parse_args():
    parser = argparse.ArgumentParser(description="MOSKV-1 Inferencia y Evaluador de Léxico Multi-Dominio")
    parser.add_argument("--model", type=str, default=None, help="Ruta o ID del modelo (MLX o HuggingFace)")
    parser.add_argument("--adapter-path", type=str, default=None, help="Ruta a adaptadores LoRA (si aplica)")
    parser.add_argument("--temp", type=float, default=0.3, help="Temperatura de generación (Default: 0.3 para precisión)")
    parser.add_argument("--max-tokens", type=int, default=256, help="Máximo de tokens por respuesta")
    parser.add_argument("--dry-run", action="store_true", help="Ejecutar solo validación de prompts y léxico sin cargar pesos")
    return parser.parse_args()

def evaluate_lexicon_density(text: str, keywords: list) -> float:
    text_lower = text.lower()
    matches = sum(1 for kw in keywords if kw.lower() in text_lower)
    return (matches / len(keywords)) * 100.0

def run_mlx_inference(model_path: str, adapter_path: str, item: dict, temp: float, max_tokens: int):
    try:
        from mlx_lm import load, generate
        print(f"\n[*] Cargando modelo MLX: {model_path}...")
        model, tokenizer = load(model_path, adapter_path=adapter_path)
        
        prompt = f"<|im_start|>system\n{item['system']}<|im_end|>\n<|im_start|>user\n{item['user']}<|im_end|>\n<|im_start|>assistant\n"
        start_t = time.time()
        response = generate(model, tokenizer, prompt=prompt, max_tokens=max_tokens, verbose=False)
        elapsed = time.time() - start_t
        
        density = evaluate_lexicon_density(response, item['keywords'])
        return response, elapsed, density
    except Exception as e:
        print(f"[!] Error en generación MLX: {e}")
        return None, 0, 0

def main():
    args = parse_args()
    print("=== [MOSKV-1 Multi-Domain Inference Test Bench & Lexicon Evaluator v2.0] ===")
    
    if args.dry_run or not args.model:
        print("[*] Modo Dry-Run / Inspección de Plantillas Activo:")
        for idx, item in enumerate(PROMPTS, 1):
            print(f"\n------------------------------------------------------------")
            print(f"📌 [{idx}/5] DOMINIO: {item['domain']}")
            print(f"  System Prompt: {item['system']}")
            print(f"  User Query:    {item['user']}")
            print(f"  Target Keywords ({len(item['keywords'])}): {', '.join(item['keywords'])}")
            print(f"------------------------------------------------------------")
        print("\n[✓] Prompts e Invariantes de evaluación listos. Pasa `--model <model_path>` para inferencia en caliente.")
        return

    print(f"[*] Modo Inferencia En Caliente | Modelo: {args.model} | Adaptador: {args.adapter_path}")
    
    results = []
    for item in PROMPTS:
        print(f"\n============================================================")
        print(f"🚀 Generando para Dominio: {item['domain']}")
        print(f"============================================================")
        
        response, elapsed, density = run_mlx_inference(args.model, args.adapter_path, item, args.temp, args.max_tokens)
        if response:
            print(f"\n--- RESPUESTA GENERADA ({elapsed:.2f}s) ---")
            print(response.strip())
            print(f"\n📊 Densidad de Léxico C5-REAL: {density:.1f}%")
            results.append({
                "domain": item["domain"],
                "elapsed_sec": round(elapsed, 2),
                "lexicon_density_pct": round(density, 1)
            })

    print("\n=== RESUMEN DE EVALUACIÓN MULTI-DOMINIO ===")
    for r in results:
        print(f"  └─ {r['domain']}: {r['elapsed_sec']}s | Densidad Léxico: {r['lexicon_density_pct']}%")

if __name__ == "__main__":
    main()
