#!/usr/bin/env python3
"""Literal, accent-insensitive corpus search with explicit source classification."""
import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
KINDS = ("primary_ocr", "interpretation", "project_document")


def strip_accents(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", text)
                   if unicodedata.category(c) != "Mn")


def load_catalog(root=BASE_DIR):
    """Validate catalog structure, coverage and repository-byte identity."""
    root = Path(root).resolve()
    texts = root / "texts"
    if not texts.is_dir() or texts.is_symlink():
        raise ValueError("texts must be a real repository directory")
    catalog = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    if not isinstance(catalog, dict) or not isinstance(catalog.get("works"), list):
        raise ValueError("invalid manifest: works must be an array")
    result, ids = {}, set()
    for work in catalog["works"]:
        if not isinstance(work, dict):
            raise ValueError("invalid manifest entry")
        ident, rel = work.get("id"), work.get("local_path")
        if not isinstance(ident, str) or not ident or ident in ids:
            raise ValueError("missing or duplicate work ID")
        if not isinstance(rel, str) or not re.fullmatch(r"texts/[^/\\]+[.](txt|md)", rel):
            raise ValueError(f"invalid relative path: {rel!r}")
        path = root / rel
        if path.is_symlink() or not path.is_file() or path.resolve().parent != texts:
            raise ValueError(f"invalid source file: {rel}")
        if path.name in result:
            raise ValueError(f"duplicate source: {rel}")
        if work.get("kind") not in KINDS or work.get("rights_status") not in (
            "unverified", "verified"
        ):
            raise ValueError(f"invalid provenance classification: {rel}")
        if work["rights_status"] == "verified" and not work.get("rights_evidence"):
            raise ValueError(f"missing rights evidence: {rel}")
        if not isinstance(work.get("git_blob_sha1"), str) or not re.fullmatch(
            r"[0-9a-f]{40}", work["git_blob_sha1"]
        ):
            raise ValueError(f"invalid Git blob ID: {rel}")
        raw = path.read_bytes()
        git_id = hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()
        if git_id != work["git_blob_sha1"]:
            raise ValueError(f"Git blob mismatch: {rel}")
        ids.add(ident)
        result[path.name] = (work, raw)
    actual = {p.name for p in texts.iterdir()
              if p.suffix in (".txt", ".md") and (p.is_file() or p.is_symlink())}
    if not result or set(result) != actual:
        raise ValueError("manifest does not cover exactly the local text files")
    return result


def search_escota(query: str, max_results_per_work: int = 5, *,
                  root=BASE_DIR, kind=None):
    if not isinstance(query, str) or not query.strip():
        raise ValueError("query must not be empty")
    if type(max_results_per_work) is not int or max_results_per_work < 1:
        raise ValueError("limit must be a positive integer")
    if kind is not None and kind not in KINDS:
        raise ValueError("invalid source kind")
    needle = strip_accents(query.strip()).casefold()
    if not needle:
        raise ValueError("query contains no searchable characters")
    results = {}
    for filename, (work, raw) in sorted(load_catalog(root).items()):
        if kind is not None and work["kind"] != kind:
            continue
        hits, total = [], 0
        # Number physical lines using universal newline translation.
        lines = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").split("\n")
        for line_no, line in enumerate(lines, 1):
            if needle in strip_accents(line).casefold():
                total += 1
                if len(hits) < max_results_per_work:
                    hits.append({"line": line_no, "text": line.strip()})
        if total:
            results[filename] = {
                "work_id": work["id"], "title": work["title"],
                "kind": work["kind"], "path": work["local_path"],
                "rights_status": work["rights_status"],
                "file_sha256": hashlib.sha256(raw).hexdigest(),
                "hits_count": len(hits), "total_matching_lines": total,
                "truncated": total > len(hits), "hits": hits,
            }
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="?")
    parser.add_argument("--kind", choices=KINDS)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--check-catalog", action="store_true")
    args = parser.parse_args()
    try:
        if args.check_catalog:
            if args.query is not None:
                parser.error("--check-catalog does not accept a query")
            catalog = load_catalog()
            print(json.dumps({"catalog": "valid", "files": len(catalog),
                              "counts": {k: sum(w["kind"] == k for w, _ in catalog.values())
                                         for k in KINDS}}, ensure_ascii=False))
            return 0
        results = search_escota(args.query, args.limit, kind=args.kind)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.error(str(exc))
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for filename, item in results.items():
            print(f'{filename} [{item["kind"]}] '
                  f'{item["hits_count"]}/{item["total_matching_lines"]} lines')
            for hit in item["hits"]:
                print(f'  L{hit["line"]}: {hit["text"]}')
        if not results:
            print("No literal matches.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
