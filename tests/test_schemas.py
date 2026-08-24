import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from dataclasses import replace

from atlas_clarus import (
    ACTIVE_MODE, EXPECTED_MASTER_SHA256, AtlasBinder, AtlasMaster,
    build_run_manifest,
)


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
        master = AtlasMaster.from_records([
            {"reference": "SOURCE", "rgb": [10, 10, 10], "lambda_v2_nm": 500, "lambda_ee_nm": 510, "delta_lambda_nm": -10},
            {"reference": "PRODUCTION", "rgb": [11, 10, 10], "lambda_v2_nm": 500, "lambda_ee_nm": 501, "delta_lambda_nm": -1},
        ])
        result = replace(
            AtlasBinder(master).bind((10, 10, 10), mode=ACTIVE_MODE),
            master_sha256=EXPECTED_MASTER_SHA256,
        )
        manifest = build_run_manifest(
            [result], input_sha256="0" * 64,
            software_name="atlas-clarus-core", software_version="0.1.0",
            layer_status={"runtime": "PASS"},
        )
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
