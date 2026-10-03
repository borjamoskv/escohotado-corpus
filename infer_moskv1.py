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

INV_POSTFIX = " Invariante: Cero adjetivos calificativos, cero peloteo, cero adverbios en -mente. Sintaxis: [Sujeto] → [Verbo] → [Objeto]."

PROMPTS = [
    {
        "domain": "Ingeniero",
        "system": "Eres Moskv-1 (Modo Ingeniería de Software & C++20/Rust)." + INV_POSTFIX,
        "user": "Explica la garantía de atómica del Sequencer Lock-Free SPSC y el Invariante CALM II'.",
        "keywords": ["lock-free", "spsc", "atomic", "calm", "ring buffer", "memoria", "exergía"]
    },
    {
        "domain": "Físico",
        "system": "Eres Moskv-1 (Modo Física & Termodinámica)." + INV_POSTFIX,
        "user": "¿Cómo afecta el borrado de información de 1 bit al consumo termodinámico mínimo (kT ln 2)?",
        "keywords": ["landauer", "entropía", "kt ln 2", "información", "termodinámica", "disipación"]
    },
    {
        "domain": "Médico",
        "system": "Eres Moskv-1 (Modo Fisiología & Neurociencia)." + INV_POSTFIX,
        "user": "Describe la modulación neurotransmisora de la dopamina en circuitos estriatales.",
        "keywords": ["dopamina", "estriado", "neurotransmisor", "sinapsis", "receptores d1/d2", "circuito"]
    },
    {
        "domain": "Músico",
        "system": "Eres Moskv-1 (Modo Teoría Musical & Acústica Físico-Matemática)." + INV_POSTFIX,
        "user": "Analiza la afinación temperada vs justa a través de las proporciones de frecuencia pitagóricas.",
        "keywords": ["frecuencia", "temperada", "pitagórica", "armónicos", "quintas", "acústica"]
    },
    {
        "domain": "Abogado",
        "system": "Eres Moskv-1 (Modo Derecho, Invariantes de Gobernanza & SCITT)." + INV_POSTFIX,
        "user": "¿Cómo valida el registro SCITT la precedencia temporal y la integridad forense de los artefactos?",
        "keywords": ["scitt", "atestación", "merkle", "no repudio", "forense", "gobernanza", "eu ai act"]
    },
    {
        "domain": "Filósofo",
        "system": "Eres Moskv-1 (Modo Ontología Monista & Termodinámica de Sistemas Complejos). Invariante Ω118: Monismo de substancia continua, emergencia y autoorganización disipativa." + INV_POSTFIX,
        "user": "Explica cómo la autoorganización disipativa en 'Caos y Orden' refuta la necesidad de un regulador exógeno centralizado.",
        "keywords": ["monismo", "substancia", "emergencia", "autoorganización", "disipativo", "orden", "caos", "dirigismo", "exergía", "landauer"]
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

def audit_grammatical_invariants(text: str):
    import re
    mentes = re.findall(r'\b\w+mente\b', text, re.IGNORECASE)
    peloteo_pats = [r'excelente', r'maravilloso', r'fascinante', r'por supuesto', r'claro que s[ií]', r'como bien']
    peloteos = []
    for p in peloteo_pats:
        if re.search(p, text, re.IGNORECASE):
            peloteos.append(p)
    return mentes, peloteos

def run_mlx_inference(model, tokenizer, item: dict, temp: float, max_tokens: int):
    try:
        from mlx_lm import generate
        from mlx_lm.sample_utils import make_sampler
        messages = [{"role": "user", "content": f"{item['system']}\n\n{item['user']}"}]
        prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        sampler = make_sampler(temp=temp)
        start_t = time.time()
        response = generate(model, tokenizer, prompt=prompt, max_tokens=max_tokens, sampler=sampler, verbose=False)
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
            print(f"📌 [{idx}/{len(PROMPTS)}] DOMINIO: {item['domain']}")
            print(f"  System Prompt: {item['system']}")
            print(f"  User Query:    {item['user']}")
            print(f"  Target Keywords ({len(item['keywords'])}): {', '.join(item['keywords'])}")
            print(f"------------------------------------------------------------")
        print("\n[✓] Prompts e Invariantes de evaluación listos. Pasa `--model <model_path>` para inferencia en caliente.")
        return

    print(f"[*] Modo Inferencia En Caliente | Modelo: {args.model} | Adaptador: {args.adapter_path}")
    from mlx_lm import load
    print(f"[*] Cargando modelo y adaptadores en memoria unificada Metal...")
    model, tokenizer = load(args.model, adapter_path=args.adapter_path)
    print(f"[✓] Modelo cargado con éxito. Iniciando benchmark multi-dominio.")
    
    results = []
    for item in PROMPTS:
        print(f"\n============================================================")
        print(f"🚀 Generando para Dominio: {item['domain']}")
        print(f"============================================================")
        
        response, elapsed, density = run_mlx_inference(model, tokenizer, item, args.temp, args.max_tokens)
        if response:
            print(f"\n--- RESPUESTA GENERADA ({elapsed:.2f}s) ---")
            print(response.strip())
            mentes, peloteos = audit_grammatical_invariants(response)
            print(f"\n📊 Densidad de Léxico C5-REAL: {density:.1f}%")
            print(f"🛡️  Auditoría Gramatical: Mentes={len(mentes)} {mentes} | Peloteos={len(peloteos)} {peloteos}")
            results.append({
                "domain": item["domain"],
                "elapsed_sec": round(elapsed, 2),
                "lexicon_density_pct": round(density, 1),
                "mentes_count": len(mentes),
                "peloteo_count": len(peloteos)
            })

    print("\n=== RESUMEN DE EVALUACIÓN MULTI-DOMINIO ===")
    for r in results:
        print(f"  └─ {r['domain']}: {r['elapsed_sec']}s | Léxico: {r['lexicon_density_pct']}% | Mentes: {r['mentes_count']} | Peloteo: {r['peloteo_count']}")

if __name__ == "__main__":
    main()
