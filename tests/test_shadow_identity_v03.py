import csv
import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "evidence" / "shadow-identity" / "v0.3"
MIGRATION = BASE / "outputs" / "identity_digest_migration_v0_2_to_v0_3.csv"
LOCK = BASE / "outputs" / "BASELINE_LOCK_v0_3.json"


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


class ShadowIdentityV03Test(unittest.TestCase):
    def test_frozen_baseline_and_migration(self):
        lock = json.loads(LOCK.read_text(encoding="utf-8"))
        self.assertEqual(lock["decision_status"], "FROZEN")
        self.assertEqual(lock["baseline_version"], "0.3")
        self.assertFalse(lock["active_master_modified"])

        old_seen, new_seen, triples = set(), set(), []
        with MIGRATION.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 13283)

        for row in rows:
            rgb = [int(row[f"reference_rgb_{channel}"]) for channel in "rgb"]
            atlas_row_id = int(row["atlas_row_id"])
            old_payload = {
                "binding_rule_version": row["binding_rule_version"],
                "master_sha256": row["atlas_master_sha256"],
                "master_version": row["master_version"],
                "reference_rgb": rgb,
                "source_atlas_row_id": atlas_row_id,
            }
            new_payload = {
                "atlas_master_sha256": row["atlas_master_sha256"],
                "atlas_row_id": atlas_row_id,
                "binding_rule_version": row["binding_rule_version"],
                "master_version": row["master_version"],
                "reference": row["reference"],
                "reference_rgb": rgb,
            }
            old_digest, new_digest = digest(old_payload), digest(new_payload)
            self.assertEqual(old_digest, row["identity_digest_v0_2"])
            self.assertEqual(new_digest, row["identity_digest_v0_3"])
            self.assertEqual(row["migration_relation"], "SUPERSEDED_BY")
            self.assertEqual(row["migration_status"], "MIGRATED_VERIFIED")
            old_seen.add(old_digest)
            new_seen.add(new_digest)
            triples.append((atlas_row_id, row["reference"], new_digest))

        self.assertEqual(len(old_seen), 13283)
        self.assertEqual(len(new_seen), 13283)
        aggregate = hashlib.sha256(
            ("\n".join(f"{i}|{reference}|{value}" for i, reference, value in sorted(triples)) + "\n").encode()
        ).hexdigest()
        self.assertEqual(aggregate, lock["aggregate_identity_sha256"])


if __name__ == "__main__":
    unittest.main()
