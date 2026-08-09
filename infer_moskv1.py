#!/usr/bin/env python3
# ==============================================================================
# MOSKV-1 MULTI-DOMAIN TEST BENCH & INFERENCE EVALUATOR
# Evaluador de respuestas multi-dominio para verificar las 5 personalidades de MOSKV-1
# ==============================================================================

import json
import sys

PROMPTS = [
    {
        "domain": "Ingeniero",
        "system": "Eres Moskv-1 (Modo Ingeniería de Software & C++20/Rust). Invariante: Cero-Anergía y exergía máxima.",
        "user": "Explica la garantía de atómica del Sequencer Lock-Free SPSC y el Invariante CALM II'."
    },
    {
        "domain": "Físico",
        "system": "Eres Moskv-1 (Modo Física & Termodinámica). Analizas el sistema mediante mecánica estadística y cotas de Landauer.",
        "user": "¿Cómo afecta el borrado de información de 1 bit al consumo termodinámico mínimo (kT ln 2)?"
    },
    {
        "domain": "Médico",
        "system": "Eres Moskv-1 (Modo Fisiología & Neurociencia). Analizas mediante homeostosis de redes neuronales y bioenergética.",
        "user": "Describe la modulación neurotransmisora de la dopamina en circuitos estriatales."
    },
    {
        "domain": "Músico",
        "system": "Eres Moskv-1 (Modo Teoría Musical & Acústica Físico-Matemática). Analizas análisis espectral y armónicos.",
        "user": "Analiza la afinación temperada vs justa a través de las proporciones de frecuencia pitagóricas."
    },
    {
        "domain": "Abogado",
        "system": "Eres Moskv-1 (Modo Derecho, Invariantes de Gobernanza & SCITT). Analizas atestaciones jurídicas y no repudio.",
        "user": "¿Cómo valida el registro SCITT la precedencia temporal y la integridad forense de los artefactos?"
    }
]

def main():
    print("=== [MOSKV-1 Multi-Domain Inference Test Bench] ===")
    for item in PROMPTS:
        print(f"\n------------------------------------------------------------")
        print(f"📌 DOMINIO: {item['domain']}")
        print(f"  System: {item['system']}")
        print(f"  User:   {item['user']}")
        print(f"------------------------------------------------------------")
    
    print("\n[✓] Muestras de prueba preparadas para evaluación de MOSKV-1.")

if __name__ == "__main__":
    main()
