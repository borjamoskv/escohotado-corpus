#!/usr/bin/env python3
# C5-REAL EXERGY CERTIFIED
"""
Escota (Antonio Escohotado) Specialized Corpus Search & Ontological Query Engine.
Scans text corpus in scratch/corpus/escota/texts for semantic hits and epistemological concepts.
"""

import sys
import os
import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = BASE_DIR / "manifest.json"
TEXTS_DIR = BASE_DIR / "texts"

def load_manifest():
    if not MANIFEST_PATH.exists():
        return {}
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def search_escota(query: str, max_results_per_work: int = 5):
    manifest = load_manifest()
    works = manifest.get("works", [])
    results = {}

    pattern = re.compile(re.escape(query), re.IGNORECASE)

    for w in works:
        file_path = Path(w["local_path"])
        if not file_path.exists():
            continue

        work_title = w["title"]
        hits = []
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line_idx, line in enumerate(f, 1):
                if pattern.search(line):
                    hits.append({
                        "line": line_idx,
                        "text": line.strip()
                    })
                    if len(hits) >= max_results_per_work:
                        break
        if hits:
            results[work_title] = {
                "category": w.get("category", "General"),
                "archive_url": w.get("archive_url", ""),
                "hits_count": len(hits),
                "hits": hits
            }

    return results

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 escota_search.py '<término_o_concepto>'")
        print("Ejemplo: python3 escota_search.py 'substancia'")
        sys.exit(1)

    query = sys.argv[1]
    res = search_escota(query)

    print(f"=== Búsqueda Epistémica en Corpus Escota: '{query}' ===")
    if not res:
        print("No se encontraron coincidencias directas.")
        return

    for work, data in res.items():
        print(f"\nObra: {work} ({data['category']})")
        print(f"URL: {data['archive_url']}")
        for h in data["hits"]:
            print(f"  [Línea {h['line']}]: {h['text']}")

if __name__ == "__main__":
    main()
