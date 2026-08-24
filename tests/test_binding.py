import unittest

from atlas_clarus import ACTIVE_MODE, POSTHOC_MODE, AtlasBinder, AtlasMaster


class BindingTests(unittest.TestCase):
    def test_rgb_distance_and_lower_row_id_tie_break(self):
        master = AtlasMaster.from_records(
            [
                {"reference": "LOWER_ID", "rgb": [9, 10, 10], "lambda_v2_nm": 500, "lambda_ee_nm": 504, "delta_lambda_nm": -4},
                {"reference": "HIGHER_ID", "rgb": [11, 10, 10], "lambda_v2_nm": 500, "lambda_ee_nm": 501, "delta_lambda_nm": -1},
            ]
        )
        result = AtlasBinder(master).bind((10, 10, 10))
        self.assertEqual(result.source_atlas_row_id, 0)
        self.assertEqual(result.production_atlas_row_id, 0)
        self.assertEqual(result.source_rgb_distance_squared, 1)

    def test_active_mode_uses_only_rgb_top_two_and_minimum_absolute_delta_lambda(self):
        master = AtlasMaster.from_records(
            [
                {"reference": "RGB_FIRST", "rgb": [10, 10, 10], "lambda_v2_nm": 500, "lambda_ee_nm": 510, "delta_lambda_nm": -10},
                {"reference": "RGB_SECOND", "rgb": [12, 10, 10], "lambda_v2_nm": 500, "lambda_ee_nm": 501, "delta_lambda_nm": -1},
                {"reference": "OUTSIDE_CORRIDOR", "rgb": [30, 10, 10], "lambda_v2_nm": 500, "lambda_ee_nm": 500, "delta_lambda_nm": 0},
            ]
        )
        result = AtlasBinder(master).bind((10, 10, 10), mode=ACTIVE_MODE)
        self.assertEqual(result.source_atlas_row_id, 0)
        self.assertEqual(result.production_atlas_row_id, 1)
        self.assertEqual(result.production_reference, "RGB_SECOND")

    def test_posthoc_mode_preserves_source_identity(self):
        master = AtlasMaster.from_records(
            [
                {"reference": "SOURCE", "rgb": [10, 10, 10], "lambda_v2_nm": 500, "lambda_ee_nm": 510, "delta_lambda_nm": -10},
                {"reference": "SECOND", "rgb": [11, 10, 10], "lambda_v2_nm": 500, "lambda_ee_nm": 500, "delta_lambda_nm": 0},
            ]
        )
        result = AtlasBinder(master).bind((10, 10, 10), mode=POSTHOC_MODE)
        self.assertEqual(result.source_atlas_row_id, 0)
        self.assertEqual(result.production_atlas_row_id, 0)

    def test_active_delta_lambda_tie_uses_lower_row_id(self):
        master = AtlasMaster.from_records(
            [
                {"reference": "LOWER_ID", "rgb": [10, 10, 10], "lambda_v2_nm": 500, "lambda_ee_nm": 505, "delta_lambda_nm": -5},
                {"reference": "HIGHER_ID", "rgb": [11, 10, 10], "lambda_v2_nm": 500, "lambda_ee_nm": 495, "delta_lambda_nm": 5},
            ]
        )
        result = AtlasBinder(master).bind((10, 10, 10), mode=ACTIVE_MODE)
        self.assertEqual(result.source_atlas_row_id, 0)
        self.assertEqual(result.production_atlas_row_id, 0)

    def test_duplicate_rgb_uses_lower_row_id(self):
        master = AtlasMaster.from_records(
            [
                {"reference": "H005_L090_C005", "rgb": [237, 224, 227], "lambda_v2_nm": 500, "lambda_ee_nm": 502, "delta_lambda_nm": -2},
                {"reference": "H360_L090_C005", "rgb": [237, 224, 227], "lambda_v2_nm": 500, "lambda_ee_nm": 501, "delta_lambda_nm": -1},
            ]
        )
        result = AtlasBinder(master).bind((237, 224, 227))
        self.assertEqual(result.source_atlas_row_id, 0)
        self.assertEqual(result.source_reference, "H005_L090_C005")

    def test_invalid_rgb_is_rejected(self):
        master = AtlasMaster.from_records(
            [{"reference": "ONLY", "rgb": [0, 0, 0], "lambda_v2_nm": 500, "lambda_ee_nm": 500, "delta_lambda_nm": 0}]
        )
        for rgb in [(-1, 0, 0), (256, 0, 0), (1.2, 0, 0), (True, 0, 0), (0, 0)]:
            with self.subTest(rgb=rgb), self.assertRaises(ValueError):
                AtlasBinder(master).bind(rgb)


if __name__ == "__main__":
    unittest.main()
