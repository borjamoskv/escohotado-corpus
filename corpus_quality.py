#!/usr/bin/env python3
"""Read-only MLX split audit and provenance gate; no semantic certification."""
import argparse
import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KINDS = {"primary_analysis", "interpretation", "technical"}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def normalize(text):
    return " ".join(unicodedata.normalize("NFC", text).split())


def question(prompt):
    if prompt.startswith("Eres Moskv-1") and "\n\n" in prompt:
        prompt = prompt.split("\n\n", 1)[1]
    return normalize(prompt).casefold()


def pair_id(prompt, completion):
    return digest(json.dumps([prompt, completion], ensure_ascii=False,
                             separators=(",", ":")).encode("utf-8"))


def read_rows(path):
    rows, errors = [], []
    try:
        raw = path.read_bytes()
        for i, line in enumerate(raw.decode("utf-8").splitlines(), 1):
            try:
                row = json.loads(line)
                if not isinstance(row, dict):
                    raise ValueError("object required")
                rows.append((i, row))
            except ValueError:
                errors.append(i)
        return rows, errors, digest(raw)
    except (OSError, UnicodeError):
        return [], [0], None


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def review_valid(row, root, cache):
    if (row.get("status") != "approved" or row.get("kind") not in KINDS
            or not all(nonempty(row.get(k)) for k in ("reviewer", "source_group", "rights_basis"))):
        return False
    evidence = row.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        return False
    for item in evidence:
        try:
            rel = Path(item["path"])
            if rel.is_absolute() or ".." in rel.parts:
                return False
            path = (root / rel).resolve()
            if not path.is_relative_to(root) or not path.is_file():
                return False
            if path not in cache:
                raw = path.read_bytes()
                cache[path] = (digest(raw), len(raw.decode("utf-8").splitlines()))
            sha, count = cache[path]
            start, end = item["start_line"], item["end_line"]
            if (sha != item["sha256"] or type(start) is not int or type(end) is not int
                    or not 1 <= start <= end <= count):
                return False
        except (KeyError, TypeError, ValueError, OSError, UnicodeError, RuntimeError):
            return False
    return True


def audit(data, source_root=ROOT):
    data, root = Path(data), Path(source_root).resolve()
    reviews, review_errors, review_hash = read_rows(data / "review.jsonl")
    by_id, invalid_reviews, cache = {}, 0, {}
    for _, review in reviews:
        rid = review.get("record_sha256")
        if (not isinstance(rid, str) or not re.fullmatch(r"[0-9a-f]{64}", rid)
                or rid in by_id or not review_valid(review, root, cache)):
            invalid_reviews += 1
            continue
        by_id[rid] = review

    stats, keys, groups = {}, {}, {}
    seen_ids = set()
    for split in ("train", "valid"):
        rows, errors, file_hash = read_rows(data / f"{split}.jsonl")
        prompts, answers, pairs, source_groups = [], [], [], set()
        missing = ocr = 0
        variants = defaultdict(set)
        for line, row in rows:
            p, a = row.get("prompt"), row.get("completion")
            if not nonempty(p) or not nonempty(a):
                errors.append(line)
                continue
            q, answer = question(p), normalize(a)
            prompts.append(q)
            answers.append(answer)
            pairs.append((normalize(p), answer))
            variants[q].add(answer)
            ocr += bool(re.search(r"\b\w{2,}-\s+\w{2,}\b", a))
            rid = pair_id(p, a)
            seen_ids.add(rid)
            review = by_id.get(rid)
            if review:
                source_groups.add(review["source_group"])
            else:
                missing += 1
        keys[split] = (prompts, answers, set(pairs))
        groups[split] = source_groups
        stats[split] = dict(rows=len(prompts), file_sha256=file_hash,
                            invalid_lines=sorted(errors), unique_questions=len(set(prompts)),
                            duplicate_pairs=len(pairs)-len(set(pairs)),
                            multi_answer_questions=sum(len(v)>1 for v in variants.values()),
                            ocr_hyphen_candidates=ocr, missing_verified_review=missing)
    t, v = keys["train"], keys["valid"]
    tq, vq = set(t[0]), set(v[0])
    cross = dict(questions=len(tq & vq), valid_rows_with_train_question=sum(q in tq for q in v[0]),
                 answers=len(set(t[1]) & set(v[1])), pairs=len(t[2] & v[2]),
                 source_groups=len(groups["train"] & groups["valid"]))
    failures = []
    for split, s in stats.items():
        for condition, label in ((not s["rows"], "empty"), (s["invalid_lines"], "invalid"),
                                 (s["duplicate_pairs"], "duplicate_pairs"),
                                 (s["missing_verified_review"], "missing_review")):
            if condition:
                failures.append(f"{split}:{label}")
    for key in ("questions", "pairs", "source_groups"):
        if cross[key]:
            failures.append(f"cross_split:{key}")
    if review_errors or invalid_reviews or set(by_id)-seen_ids:
        failures.append("review:invalid_missing_or_stale")
    return dict(splits=stats, cross_split=cross, review_file_sha256=review_hash,
                review_errors=review_errors, invalid_reviews=invalid_reviews,
                stale_reviews=len(set(by_id)-seen_ids), gate_failures=failures,
                gate_passed=not failures, semantic_certification=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=ROOT / "data_mlx")
    parser.add_argument("--source-root", type=Path, default=ROOT)
    parser.add_argument("--gate", action="store_true", help="Exit 1 on any gate failure")
    args = parser.parse_args()
    report = audit(args.data, args.source_root)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return int(args.gate and not report["gate_passed"])


if __name__ == "__main__":
    raise SystemExit(main())
