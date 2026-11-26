import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from audit_21_swarm_dataset import audit, merkle_root
from escota_search import load_catalog, search_escota


class CorpusTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "texts").mkdir()
        self.chunk = "  Energía, caos y orden.\n" * 40 + "  "
        self.add_source("a.txt", self.chunk, "primary_ocr")
        self.add_source("b.md", "Energía artificial\n", "project_document")
        self.dataset = self.root / "fixture.jsonl"

    def add_source(self, name, content, kind):
        path = self.root / "texts" / name
        raw = content.encode("utf-8")
        path.write_bytes(raw)
        manifest = self.root / "manifest.json"
        data = json.loads(manifest.read_text()) if manifest.exists() else {"works": []}
        data["works"].append({
            "id": name, "title": name, "local_path": f"texts/{name}", "kind": kind,
            "rights_status": "unverified",
            "git_blob_sha1": hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
        })
        manifest.write_text(json.dumps(data), encoding="utf-8")

    def record(self):
        return {
            "messages": [{"role": "system", "content": "fixture"},
                         {"role": "user", "content": "question"},
                         {"role": "assistant", "content": self.chunk.strip()}],
            "metadata": {"source": "a.txt", "zone": 0,
                         "sha256": hashlib.sha256(self.chunk.encode()).hexdigest()},
        }

    def write_records(self, *records):
        self.dataset.write_text("".join(json.dumps(r) + "\n" for r in records),
                                encoding="utf-8")

    def test_search_accents_filter_and_true_count(self):
        result = search_escota("ENERGIA", 2, root=self.root, kind="primary_ocr")
        self.assertEqual(list(result), ["a.txt"])
        self.assertEqual(result["a.txt"]["total_matching_lines"], 40)
        self.assertEqual(result["a.txt"]["hits_count"], 2)
        self.assertTrue(result["a.txt"]["truncated"])
        self.assertEqual(result["a.txt"]["hits"][0]["line"], 1)

    def test_invalid_query_and_limit(self):
        for query, limit in [("", 5), (" ", 1), ("foo", 0)]:
            with self.assertRaises(ValueError):
                search_escota(query, limit, root=self.root)

    def test_catalog_rejects_modified_source(self):
        (self.root / "texts" / "a.txt").write_text("changed")
        with self.assertRaisesRegex(ValueError, "Git blob mismatch"):
            load_catalog(self.root)

    def test_catalog_rejects_unlisted_source(self):
        (self.root / "texts" / "unknown.txt").write_text("extra")
        with self.assertRaisesRegex(ValueError, "cover exactly"):
            load_catalog(self.root)

    def test_audit_checks_untrimmed_hash_and_trimmed_payload(self):
        rec = self.record()
        self.write_records(rec)
        result = audit(self.dataset, root=self.root)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["verified_source_records"], 1)
        self.assertEqual(result["merkle_root_sha256"], rec["metadata"]["sha256"])

    def test_audit_rejects_payload_tampering(self):
        rec = self.record()
        rec["messages"][2]["content"] = "fabricated"
        self.write_records(rec)
        result = audit(self.dataset, root=self.root)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["errors"], {"assistant_payload_mismatch": 1})
        self.assertIsNone(result["merkle_root_sha256"])

    def test_audit_rejects_wrong_hash(self):
        rec = self.record()
        rec["metadata"]["sha256"] = "0" * 64
        self.write_records(rec)
        self.assertEqual(audit(self.dataset, root=self.root)["errors"],
                         {"source_hash_mismatch": 1})

    def test_audit_rejects_duplicate(self):
        rec = self.record()
        self.write_records(rec, rec)
        result = audit(self.dataset, root=self.root)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["unique_hashes"], 1)

    def test_audit_rejects_empty_and_malformed(self):
        self.dataset.write_text("")
        self.assertEqual(audit(self.dataset, root=self.root)["errors"], {"empty_dataset": 1})
        self.dataset.write_text("{bad\n")
        self.assertEqual(audit(self.dataset, root=self.root)["errors"], {"invalid_json": 1})

    def test_merkle_odd_leaf(self):
        h = lambda x: hashlib.sha256(x).digest()
        a, b, c = h(b"a"), h(b"b"), h(b"c")
        self.assertEqual(merkle_root([a, b, c]), h(h(a+b) + h(c+c)).hex())
        self.assertIsNone(merkle_root([]))


if __name__ == "__main__":
    unittest.main()
