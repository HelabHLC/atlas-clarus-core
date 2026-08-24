import json
import os
from pathlib import Path
import unittest

from atlas_clarus import ACTIVE_MODE, EXPECTED_MASTER_SHA256, AtlasBinder, AtlasMaster


MASTER_ENV = "ATLAS_CLARUS_MASTER_PATH"
FIXTURES_PATH = Path(__file__).parent / "fixtures" / "real_master_regressions.json"


class FrozenMasterTests(unittest.TestCase):
    @unittest.skipUnless(os.getenv(MASTER_ENV), f"Set {MASTER_ENV} for the frozen-master integration test")
    def test_frozen_master_posthoc_regression_matrix(self):
        master = AtlasMaster.load(Path(os.environ[MASTER_ENV]))
        self.assertEqual(master.sha256, EXPECTED_MASTER_SHA256)
        fixtures = json.loads(FIXTURES_PATH.read_text(encoding="utf-8"))["posthoc"]
        for fixture in fixtures:
            with self.subTest(input_rgb=fixture["input_rgb"]):
                result = AtlasBinder(master).bind(tuple(fixture["input_rgb"]))
                self.assertEqual(result.source_atlas_row_id, fixture["source_atlas_row_id"])
                self.assertEqual(result.source_reference, fixture["source_reference"])
                self.assertEqual(result.source_rgb, tuple(fixture["source_rgb"]))
                self.assertEqual(
                    result.source_rgb_distance_squared,
                    fixture["source_rgb_distance_squared"],
                )

    @unittest.skipUnless(os.getenv(MASTER_ENV), f"Set {MASTER_ENV} for the frozen-master integration test")
    def test_frozen_master_active_two_id_regression(self):
        master = AtlasMaster.load(Path(os.environ[MASTER_ENV]))
        fixtures = json.loads(FIXTURES_PATH.read_text(encoding="utf-8"))["active"]
        for fixture in fixtures:
            with self.subTest(input_rgb=fixture["input_rgb"]):
                result = AtlasBinder(master).bind(tuple(fixture["input_rgb"]), mode=ACTIVE_MODE)
                self.assertEqual(result.source_atlas_row_id, fixture["source_atlas_row_id"])
                self.assertEqual(result.production_atlas_row_id, fixture["production_atlas_row_id"])
                self.assertNotEqual(result.source_atlas_row_id, result.production_atlas_row_id)


if __name__ == "__main__":
    unittest.main()
