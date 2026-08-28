import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIR = ROOT / "evidence" / "p02-brand-colour-conflict"


class P02EvidencePackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((PACKAGE_DIR / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
        cls.records = []
        for item in cls.manifest["records"]:
            path = PACKAGE_DIR / item["filename"]
            cls.records.append((item, json.loads(path.read_text(encoding="utf-8")), path))

    def test_every_record_matches_manifest_sha256(self):
        for item, _record, path in self.records:
            with self.subTest(path=path.name):
                actual = hashlib.sha256(path.read_bytes()).hexdigest()
                self.assertEqual(actual, item["sha256"])

    def test_gate_sequence_is_complete_and_ordered(self):
        self.assertEqual([item["gate"] for item, _record, _path in self.records], [1, 2, 3, 4, 5])
        self.assertEqual([record["gate"] if isinstance(record["gate"], int) else int(record["gate"]["id"].rsplit("_", 1)[1]) for _item, record, _path in self.records], [1, 2, 3, 4, 5])

    def test_gates_one_to_three_preserve_unresolved_unfrozen_state(self):
        for _item, record, _path in self.records[:3]:
            with self.subTest(gate=record["gate"]):
                self.assertEqual(record["status"]["source_authority"], "UNRESOLVED")
                self.assertEqual(record["status"]["freeze_status"], "NOT_FROZEN_EXPERIMENTAL")
                self.assertEqual(record["status"]["production_feasibility"], "NOT_EXECUTED")
                self.assertEqual(record["status"]["measured_qc_status"], "NOT_MEASURED")

    def test_gate_three_candidates_are_non_binding(self):
        record = self.records[2][1]
        self.assertEqual(record["status"]["candidate_routes"], "COMPLETED_NON_BINDING")
        self.assertTrue(record["status"]["route_divergence"])
        self.assertIsNone(record["authority_state"]["selected_representation"])
        self.assertIsNone(record["authority_state"]["source_atlas_row_id"])
        self.assertEqual(record["normative_binding_status"], "NO_SOURCE_IDENTITY_FROZEN")
        self.assertFalse(record["execution_boundaries"]["normative_source_identity_assigned"])

    def test_gate_four_does_not_select_authority_from_candidate_results(self):
        record = self.records[3][1]
        decision = record["formal_decision"]
        self.assertEqual(decision["SOURCE_AUTHORITY"], "UNRESOLVED")
        self.assertIsNone(decision["SELECTED_REPRESENTATION"])
        self.assertIsNone(decision["source_atlas_row_id"])
        self.assertEqual(decision["FREEZE_STATUS"], "NOT_FROZEN_EXPERIMENTAL")
        self.assertFalse(record["candidate_result_separation"]["candidate_distance_used_to_choose_authority"])

    def test_gate_five_activates_method_hold_not_qc_block(self):
        record = self.records[4][1]
        result = record["formal_result"]
        self.assertEqual(result["AUTHORITY_RESOLUTION_HOLD"], "ACTIVE")
        self.assertEqual(result["production_processing"], "NOT_AUTHORIZED")
        self.assertEqual(result["measured_qc_status"], "NOT_MEASURED")
        self.assertIn("not a measured QC status", record["gate"]["clarification"])
        self.assertEqual(record["state_transition"]["forbidden_direct_transition"], "AUTHORITY_RESOLUTION_HOLD_ACTIVE_TO_PRODUCTION_OR_QC")

    def test_package_terminal_state_matches_gate_five(self):
        final = self.manifest["final_state"]
        gate_five = self.records[4][1]["formal_result"]
        self.assertEqual(final["source_authority"], gate_five["SOURCE_AUTHORITY"])
        self.assertEqual(final["freeze_status"], gate_five["FREEZE_STATUS"])
        self.assertEqual(final["authority_resolution_hold"], gate_five["AUTHORITY_RESOLUTION_HOLD"])
        self.assertEqual(final["production_processing"], gate_five["production_processing"])
        self.assertEqual(final["measured_qc_status"], gate_five["measured_qc_status"])


if __name__ == "__main__":
    unittest.main()
