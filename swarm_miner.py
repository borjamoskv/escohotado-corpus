#!/usr/bin/env python3
# C5-REAL EXERGY CERTIFIED
# LoRA Swarm Pipeline: Escohotado Corpus (Ω118)

import os
import hashlib
import json
import multiprocessing as mp
from pathlib import Path

# Paths
BASE_DIR = Path("/Users/borjafernandezangulo/10_PROJECTS/escohotado-corpus")
TEXTS_DIR = BASE_DIR / "texts"
OUTPUT_FILE = BASE_DIR / "moskv1_filosofo_sharegpt.jsonl"

SYSTEM_PROMPT = (
    "Eres el núcleo analítico de CORTEX, especializado en la ontología monista "
    "de Antonio Escohotado, termodinámica de sistemas complejos y exergía. "
    "Tus razonamientos operan bajo el Invariante Tripartito Ω118: (1) Monismo de Substancia Continua, "
    "(2) Emergencia No Lineal sin Diseñador Exógeno y (3) Rechazo del dirigismo."
)

USER_PROMPTS = [
    "Sintetiza la postura filosófica subyacente en el siguiente postulado, conectándola con la termodinámica de sistemas complejos.",
    "Analiza el siguiente fragmento bajo la lente del Invariante Ω118 (Monismo, Emergencia y Rechazo del dirigismo).",
    "Extrae las ideas principales sobre autoorganización y substancia del siguiente texto:",
    "Interpreta esta reflexión desde una perspectiva filosófico-materialista purgada de dualismos:"
]

def chunk_text(text, chunk_size=2500, overlap=300):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += (chunk_size - overlap)
    return chunks

def process_zone(args):
    filename, zone_index, chunk, user_prompt_idx = args
    
    # [DEDUPLICACIÓN SHA-256]
    chunk_hash = hashlib.sha256(chunk.encode('utf-8')).hexdigest()
    
    # [FORMATO CHATML / SHAREGPT]
    # Llama-Factory and Unsloth natively support OpenAI's 'messages' format (ChatML schema)
    user_prompt = USER_PROMPTS[user_prompt_idx % len(USER_PROMPTS)]
    
    # For a real dataset, the user asks the question and the assistant provides the text.
    # Since we are mining raw text, we simulate the text as the assistant's deep analytical response.
    record = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": chunk.strip()}
        ],
        "metadata": {
            "source": filename,
            "zone": zone_index,
            "sha256": chunk_hash
        }
    }
    return record, chunk_hash

def main():
    print(f"[*] Iniciando LoRA Swarm Pipeline (Invariante Ω118)")
    files = list(TEXTS_DIR.glob("*.txt")) + list(TEXTS_DIR.glob("*.md"))
    if not files:
        print("[!] No se encontraron textos en el directorio.")
        return

    # [LECTURA ÚNICA] Cero anergía de I/O
    tasks = []
    for filepath in files:
        print(f"[*] Leyendo en memoria: {filepath.name}")
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        chunks = chunk_text(content)
        print(f"[*] {filepath.name}: segmentado en {len(chunks)} N-Zonas.")
        
        for i, chunk in enumerate(chunks):
            # Only keep chunks that are substantial (avoiding short garbage at ends)
            if len(chunk.strip()) > 500:
                tasks.append((filepath.name, i, chunk, i))

    print(f"[*] Total de subagentes (chunks) programados: {len(tasks)}")
    
    import sys
    num_cores = 21
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        num_cores = int(sys.argv[1])
    print(f"[*] Orquestando enjambre PxS con {num_cores} agentes autónomos paralelos...")
    
    unique_hashes = set()
    records = []
    
    with mp.Pool(num_cores) as pool:
        results = pool.map(process_zone, tasks)
        
        for record, chunk_hash in results:
            if chunk_hash not in unique_hashes:
                unique_hashes.add(chunk_hash)
                records.append(record)

    print(f"[*] Deduplicación completa. Registros únicos recuperados: {len(records)}")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
            
    print(f"[*] Dataset ChatML/ShareGPT emitido con éxito en: {OUTPUT_FILE.name}")
    print("[*] ¡Colapso epistémico finalizado! Exergía conservada.")

if __name__ == "__main__":
    main()
