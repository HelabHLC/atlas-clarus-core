import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from atlas_clarus import ACTIVE_MODE, AtlasBinder, AtlasMaster


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"


def load_schema(name):
    with (SCHEMA_DIR / name).open(encoding="utf-8") as handle:
        return json.load(handle)


class EvidenceSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.binding_schema = load_schema("binding-record.schema.json")
        cls.run_schema = load_schema("run-manifest.schema.json")
        binding_resource = Resource.from_contents(cls.binding_schema)
        cls.registry = Registry().with_resource("binding-record.schema.json", binding_resource)

    def binding_record(self):
        master = AtlasMaster.from_records([
            {"reference": "SOURCE", "rgb": [10, 10, 10], "lambda_v2_nm": 500, "lambda_ee_nm": 510, "delta_lambda_nm": -10},
            {"reference": "PRODUCTION", "rgb": [11, 10, 10], "lambda_v2_nm": 500, "lambda_ee_nm": 501, "delta_lambda_nm": -1},
        ])
        return AtlasBinder(master).bind((10, 10, 10), mode=ACTIVE_MODE).to_record()

    def test_generated_binding_record_validates(self):
        Draft202012Validator(self.binding_schema).validate(self.binding_record())

    def test_complete_active_run_manifest_validates(self):
        record = self.binding_record()
        record["master_sha256"] = "8283ab91b10f89ac758d09ecf5fb4d6343536600a06dd468b1cc1ecf4ec747c4"
        manifest = {
            "schema_id": "ATLAS_CLARUS_RUN_MANIFEST_V0_1_0",
            "workflow_version": "3.4.0",
            "software": {"name": "atlas-clarus-core", "version": "0.1.0"},
            "input": {"authority": "DOCUMENTED_8_BIT_SRGB", "sha256": "0" * 64},
            "master": {
                "filename": "atlas_master__active_master__v2_illumext.pkl",
                "sha256": "8283ab91b10f89ac758d09ecf5fb4d6343536600a06dd468b1cc1ecf4ec747c4",
                "row_count": 13283,
            },
            "operation": {
                "reference_variant": ACTIVE_MODE,
                "k": "UNLIMITED",
                "seed": 42,
                "delta_lambda_mode": "ACTIVE",
                "candidate_corridor": "RGB_TOP_2",
                "candidate_count": 2,
                "production_reference_selection": "MIN_ABS_DELTA_LAMBDA_THEN_LOWER_ATLAS_ROW_ID",
                "deltaE_in_selection": False,
            },
            "bindings": [record],
            "layer_status": {
                "runtime": "PASS", "persistence": "NOT_EVIDENCED",
                "cross_system": "NOT_EVIDENCED", "device": "NOT_PROVIDED",
                "measured_qc": "NOT_MEASURED",
            },
        }
        Draft202012Validator(self.run_schema, registry=self.registry).validate(manifest)

    def test_active_manifest_rejects_posthoc_corridor(self):
        operation = {
            "reference_variant": ACTIVE_MODE,
            "k": "UNLIMITED", "seed": 42, "delta_lambda_mode": "ACTIVE",
            "candidate_corridor": "SOURCE_ONLY", "candidate_count": 2,
            "production_reference_selection": "MIN_ABS_DELTA_LAMBDA_THEN_LOWER_ATLAS_ROW_ID",
            "deltaE_in_selection": False,
        }
        operation_schema = self.run_schema["properties"]["operation"]
        self.assertFalse(Draft202012Validator(operation_schema).is_valid(operation))


if __name__ == "__main__":
    unittest.main()
