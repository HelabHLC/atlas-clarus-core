from dataclasses import replace
import unittest

from atlas_clarus import (
    ACTIVE_MODE,
    EXPECTED_MASTER_SHA256,
    POSTHOC_MODE,
    AtlasBinder,
    AtlasMaster,
    EvidenceContractError,
    build_run_manifest,
)


class RunManifestTests(unittest.TestCase):
    def setUp(self):
        master = AtlasMaster.from_records([
            {"reference": "SOURCE", "rgb": [10, 10, 10], "lambda_v2_nm": 500, "lambda_ee_nm": 510, "delta_lambda_nm": -10},
            {"reference": "PRODUCTION", "rgb": [11, 10, 10], "lambda_v2_nm": 500, "lambda_ee_nm": 501, "delta_lambda_nm": -1},
        ])
        binder = AtlasBinder(master)
        self.active = replace(binder.bind((10, 10, 10), mode=ACTIVE_MODE), master_sha256=EXPECTED_MASTER_SHA256)
        self.posthoc = replace(binder.bind((10, 10, 10), mode=POSTHOC_MODE), master_sha256=EXPECTED_MASTER_SHA256)

    def test_active_manifest_aggregates_two_id_evidence(self):
        manifest = build_run_manifest(
            [self.active, self.active, self.active],
            input_sha256="a" * 64,
            software_name="atlas-clarus-core",
            software_version="0.1.0",
        )
        self.assertEqual(manifest["two_id_evidence"]["total_pixels"], 3)
        mapping = manifest["two_id_evidence"]["mapping"][0]
        self.assertEqual(mapping["pixel_count"], 3)
        self.assertEqual(mapping["pixel_fraction"], 1.0)
        self.assertEqual(mapping["production_rgb_rank"], 2)
        self.assertEqual(mapping["selection_reason"], "MIN_ABS_DELTA_LAMBDA_WITHIN_RGB_TOP_2")
        self.assertEqual(len(manifest["bindings"]), 1)

    def test_posthoc_manifest_documents_source_only_operation(self):
        manifest = build_run_manifest(
            [self.posthoc], input_sha256="b" * 64,
            software_name="atlas-clarus-core", software_version="0.1.0",
        )
        self.assertEqual(manifest["operation"]["candidate_corridor"], "SOURCE_ONLY")
        self.assertEqual(manifest["two_id_evidence"]["mapping"][0]["production_rgb_rank"], 1)
        self.assertEqual(manifest["two_id_evidence"]["mapping"][0]["selection_reason"], "SOURCE_IDENTITY")

    def test_manifest_rejects_mixed_modes(self):
        with self.assertRaises(EvidenceContractError):
            build_run_manifest(
                [self.active, self.posthoc], input_sha256="c" * 64,
                software_name="atlas-clarus-core", software_version="0.1.0",
            )

    def test_manifest_rejects_unbound_master(self):
        with self.assertRaises(EvidenceContractError):
            build_run_manifest(
                [replace(self.active, master_sha256="SYNTHETIC_TEST_MASTER")],
                input_sha256="d" * 64,
                software_name="atlas-clarus-core", software_version="0.1.0",
            )

    def test_manifest_rejects_invalid_input_hash(self):
        with self.assertRaises(EvidenceContractError):
            build_run_manifest(
                [self.active], input_sha256="not-a-hash",
                software_name="atlas-clarus-core", software_version="0.1.0",
            )


if __name__ == "__main__":
    unittest.main()
