# Corpus quality gate

The current MLX dataset is legacy material, not a reviewed training corpus. Preserve it unchanged until curation. The audit distinguishes byte-level provenance from semantic or legal certification.

## Usage

```sh
python3 corpus_quality.py --data data_mlx
python3 corpus_quality.py --data data_mlx --gate
```

The second command returns a nonzero exit status when the gate fails. The MLX launcher now invokes this gate on the requested data directory and will not silently regenerate legacy data.

## Review manifest

Place review.jsonl alongside train.jsonl and valid.jsonl. Each reviewed record requires:

- record_sha256: SHA-256 of the UTF-8 JSON array [prompt, completion], using ensure_ascii=False and separators=(",", ":").
- status: approved (after actual human review).
- kind: primary_analysis, interpretation or technical.
- reviewer: reviewer identifier.
- source_group: stable identifier for the evidence group, assigned before splitting.
- rights_basis: documented rights basis, not a generic assertion.
- evidence: nonempty array of objects with path (relative to source root), sha256 (full source file), start_line and end_line (inclusive, one-based).

Do not auto-approve records. Keep primary texts, commentary and technical analogies distinct. Verify source alignment, attribution, completeness and rights before approval. Use group-disjoint splits and hold out independently authored evaluation questions. The audit detects normalized exact question/pair leakage and declared evidence group overlap; it does not prove semantic correctness or detect all paraphrased leakage. OCR hyphen candidates and multiple-answer questions are review signals, not proof of defects.

Historical builders may regenerate contaminated outputs. Do not use them to replace curated data without reviewing their extraction and alignment logic first.
