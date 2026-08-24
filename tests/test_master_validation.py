import unittest

import pandas as pd

from atlas_clarus import AtlasMaster, MasterValidationError


def record(reference="VALID", *, lambda_v2=500.0, lambda_ee=501.0, delta_lambda=-1.0):
    return {
        "reference": reference,
        "rgb": [10, 20, 30],
        "lambda_v2_nm": lambda_v2,
        "lambda_ee_nm": lambda_ee,
        "delta_lambda_nm": delta_lambda,
    }


class MasterValidationTests(unittest.TestCase):
    def test_non_finite_lambda_values_are_rejected(self):
        for field in ("lambda_v2_nm", "lambda_ee_nm", "delta_lambda_nm"):
            invalid = record()
            invalid[field] = float("nan")
            with self.subTest(field=field), self.assertRaises(MasterValidationError):
                AtlasMaster.from_records([invalid])

    def test_delta_lambda_relation_uses_documented_tolerance(self):
        AtlasMaster.from_records([
            record(delta_lambda=-0.9995),
        ])
        with self.assertRaises(MasterValidationError):
            AtlasMaster.from_records([
                record(delta_lambda=-0.99),
            ])

    def test_frozen_contract_rejects_wrong_row_count(self):
        master = AtlasMaster(frame=pd.DataFrame.from_records([record()]), sha256="test")
        with self.assertRaisesRegex(MasterValidationError, "row count mismatch"):
            master.validate(require_frozen_contract=True)

    def test_frozen_contract_rejects_wrong_index(self):
        frame = pd.DataFrame.from_records(
            [record(reference=f"R{row_id}") for row_id in range(13_283)]
        )
        frame.index = pd.RangeIndex(1, 13_284)
        master = AtlasMaster(frame=frame, sha256="test")
        with self.assertRaisesRegex(MasterValidationError, "RangeIndex"):
            master.validate(require_frozen_contract=True)


if __name__ == "__main__":
    unittest.main()
