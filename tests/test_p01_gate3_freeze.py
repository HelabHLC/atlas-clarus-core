import importlib.util
import unittest
from pathlib import Path


class P01Gate3FreezeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        repo_root = Path(__file__).resolve().parents[1]
        verifier_path = (
            repo_root
            / "evidence/p01-input-spaces/gate-3/verify_p01_gate3_freeze.py"
        )
        spec = importlib.util.spec_from_file_location("p01_gate3_verifier", verifier_path)
        if spec is None or spec.loader is None:
            raise RuntimeError("Could not load P01 Gate-3 verifier")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        cls.verifier = module

    def test_freeze_chain_is_verified(self):
        report = self.verifier.verify()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["gate2_selected_atlas_row_id"], 5082)
        self.assertEqual(report["persisted_source_atlas_row_id"], 5082)
        self.assertEqual(report["readback_source_atlas_row_id"], 5082)
        self.assertEqual(report["freeze_status"], "FROZEN")
        self.assertEqual(report["verification_status"], "VERIFIED")
        self.assertFalse(report["colour_matching_reexecuted"])

    def test_required_integrity_checks_pass(self):
        report = self.verifier.verify()
        required = {
            "gate2_predecessor_sha256",
            "binding_core_blob_unchanged",
            "handoff_gate2_to_freeze",
            "persistent_readback",
            "binding_result_in_memory_mutation_blocked",
            "downstream_separate_production_id_preserves_source",
            "tampered_canonical_digest_detected",
            "tampered_source_id_rejected",
        }
        self.assertTrue(required.issubset(report["checks"]))
        self.assertTrue(all(report["checks"][name] == "PASS" for name in required))


if __name__ == "__main__":
    unittest.main()
