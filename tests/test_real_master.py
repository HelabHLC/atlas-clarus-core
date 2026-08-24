import os
from pathlib import Path
import unittest

from atlas_clarus import ACTIVE_MODE, EXPECTED_MASTER_SHA256, AtlasBinder, AtlasMaster


MASTER_ENV = "ATLAS_CLARUS_MASTER_PATH"


class FrozenMasterTests(unittest.TestCase):
    @unittest.skipUnless(os.getenv(MASTER_ENV), f"Set {MASTER_ENV} for the frozen-master integration test")
    def test_frozen_master_and_known_reference(self):
        master = AtlasMaster.load(Path(os.environ[MASTER_ENV]))
        self.assertEqual(master.sha256, EXPECTED_MASTER_SHA256)
        result = AtlasBinder(master).bind((170, 195, 60))
        self.assertEqual(result.source_atlas_row_id, 4085)
        self.assertEqual(result.source_reference, "H110_L075_C065")
        self.assertEqual(result.source_rgb, (170, 195, 60))
        self.assertEqual(result.source_rgb_distance_squared, 0)

    @unittest.skipUnless(os.getenv(MASTER_ENV), f"Set {MASTER_ENV} for the frozen-master integration test")
    def test_frozen_master_active_two_id_regression(self):
        master = AtlasMaster.load(Path(os.environ[MASTER_ENV]))
        result = AtlasBinder(master).bind((170, 195, 60), mode=ACTIVE_MODE)
        self.assertEqual(result.source_atlas_row_id, 4085)
        self.assertEqual(result.production_atlas_row_id, 3892)
        self.assertNotEqual(result.source_atlas_row_id, result.production_atlas_row_id)


if __name__ == "__main__":
    unittest.main()
