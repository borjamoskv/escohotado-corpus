#!/usr/bin/env python3
# C5-REAL EXERGY CERTIFIED — ACCENT INSENSITIVE SEARCH ENGINE
"""
Escota (Antonio Escohotado & C5-REAL) Ontological Query & Search Engine.
Scans text corpus in texts/ for semantic hits, supporting accent-insensitive matching.
"""

import sys
import os
import json
import re
import unicodedata
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TEXTS_DIR = BASE_DIR / "texts"

def strip_accents(text: str) -> str:
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

def search_escota(query: str, max_results_per_work: int = 5):
    results = {}
    normalized_query = strip_accents(query).lower()
    pattern = re.compile(re.escape(normalized_query), re.IGNORECASE)

    files = sorted(list(TEXTS_DIR.glob("*.txt")) + list(TEXTS_DIR.glob("*.md")))

    for file_path in files:
        work_title = file_path.name
        hits = []
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line_idx, line in enumerate(f, 1):
                norm_line = strip_accents(line).lower()
                if pattern.search(norm_line):
                    hits.append({
                        "line": line_idx,
                        "text": line.strip()
                    })
                    if len(hits) >= max_results_per_work:
                        break
        if hits:
            results[work_title] = {
                "hits_count": len(hits),
                "hits": hits
            }

    return results

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 escota_search.py '<término_o_concepto>'")
        print("Ejemplo: python3 escota_search.py 'termodinamica'")
        sys.exit(1)

    query = sys.argv[1]
    res = search_escota(query)

    print(f"=== Búsqueda Epistémica en Corpus Escota / C5-REAL: '{query}' ===")
    if not res:
        print("No se encontraron coincidencias directas.")
        return

    total_hits = sum(d['hits_count'] for d in res.values())
    print(f"✅ Encontradas coincidencias en {len(res)} archivos ({total_hits} fragmentos):\n")

    for work, data in res.items():
        print(f"📄 Archivo: {work}")
        for h in data["hits"]:
            print(f"   [Línea {h['line']}]: {h['text']}")
        print()

if __name__ == "__main__":
    main()
