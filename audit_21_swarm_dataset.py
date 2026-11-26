#!/usr/bin/env python3
"""Read-only audit of legacy OCR-extraction records and their source lineage."""
import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

from escota_search import BASE_DIR, load_catalog

DATASET_FILE = BASE_DIR / "moskv1_filosofo_sharegpt.jsonl"
CHUNK_SIZE = 2500
STRIDE = 2200
ROLES = ["system", "user", "assistant"]


def merkle_root(leaves):
    """Legacy ordered SHA-256 tree; duplicate the last node at odd levels."""
    level = list(leaves)
    if not level:
        return None
    while len(level) > 1:
        if len(level) % 2:
            level.append(level[-1])
        level = [hashlib.sha256(level[i] + level[i+1]).digest()
                 for i in range(0, len(level), 2)]
    return level[0].hex()


def audit(dataset=DATASET_FILE, *, root=BASE_DIR):
    catalog = load_catalog(root)
    sources = {name: raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
               for name, (_, raw) in catalog.items()}
    total = role_valid = token_estimate = verified = 0
    leaves, hashes, payload_hashes = [], set(), set()
    breakdown, errors = Counter(), Counter()
    examples = []

    def issue(code, line):
        errors[code] += 1
        if len(examples) < 25:
            examples.append({"line": line, "error": code})

    with Path(dataset).open(encoding="utf-8") as stream:
        for line_no, line in enumerate(stream, 1):
            total += 1
            try:
                rec = json.loads(line)
            except ValueError:
                issue("invalid_json", line_no)
                continue
            if not isinstance(rec, dict):
                issue("invalid_record", line_no)
                continue
            msgs = rec.get("messages")
            if not (isinstance(msgs, list) and len(msgs) == 3
                    and all(isinstance(m, dict) and isinstance(m.get("content"), str)
                            and m["content"].strip() for m in msgs)
                    and [m.get("role") for m in msgs] == ROLES):
                issue("invalid_roles_or_content", line_no)
                continue
            role_valid += 1
            token_estimate += int(sum(len(m["content"].split()) for m in msgs) * 1.3)
            meta = rec.get("metadata")
            if not isinstance(meta, dict):
                issue("missing_metadata", line_no)
                continue
            source, zone = meta.get("source"), meta.get("zone")
            if not isinstance(source, str) or source not in sources:
                issue("unknown_source", line_no)
                continue
            if type(zone) is not int or zone < 0:
                issue("invalid_zone", line_no)
                continue
            text = sources[source]
            offset = zone * STRIDE
            if offset >= len(text):
                issue("zone_out_of_range", line_no)
                continue
            chunk = text[offset:offset + CHUNK_SIZE]
            if len(chunk.strip()) <= 500:
                issue("short_source_chunk", line_no)
                continue
            digest = hashlib.sha256(chunk.encode("utf-8")).digest()
            if meta.get("sha256") != digest.hex():
                issue("source_hash_mismatch", line_no)
                continue
            if msgs[2]["content"] != chunk.strip():
                issue("assistant_payload_mismatch", line_no)
                continue
            verified += 1
            breakdown[source] += 1
            leaves.append(digest)
            if digest in hashes:
                issue("duplicate_source_chunk", line_no)
            hashes.add(digest)
            payload = hashlib.sha256(msgs[2]["content"].encode("utf-8")).digest()
            if payload in payload_hashes:
                issue("duplicate_assistant_payload", line_no)
            payload_hashes.add(payload)
    if not total:
        issue("empty_dataset", 0)
    return {
        "status": "PASS" if not errors else "FAIL",
        "scope": "legacy extraction integrity, not authorship, licensing or answer quality",
        "total_n_zones": total, "verified_source_records": verified,
        "unique_hashes": len(hashes),
        "unique_assistant_payloads": len(payload_hashes),
        "uniqueness_ratio": len(hashes) / total if total else 0,
        "role_structure_validity": role_valid / total if total else 0,
        "total_estimated_tokens": token_estimate,
        "token_estimator": "floor(words_per_record * 1.3), not tokenizer output",
        "sources_count": len(breakdown), "sources_breakdown": dict(sorted(breakdown.items())),
        "merkle_root_sha256": merkle_root(leaves) if verified == total and total else None,
        "errors": dict(sorted(errors.items())), "error_examples": examples,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DATASET_FILE)
    parser.add_argument("--output", type=Path, help="Create a new report; never overwrite.")
    args = parser.parse_args()
    try:
        report = audit(args.dataset)
        encoded = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            with args.output.open("x", encoding="utf-8") as stream:
                stream.write(encoded)
        print(encoded, end="")
        return 0 if report["status"] == "PASS" else 1
    except (ValueError, OSError, TypeError, KeyError) as exc:
        print(f"Audit failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
