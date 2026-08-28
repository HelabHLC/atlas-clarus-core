from copy import deepcopy
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator

from atlas_clarus import build_authority_hold_record


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"


def load_schema(name):
    with (SCHEMA_DIR / name).open(encoding="utf-8") as handle:
        return json.load(handle)


class SourceAuthoritySchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.decision_schema = load_schema("source-authority-decision.schema.json")
        cls.input_schema = load_schema("recognised-input-record.schema.json")
        cls.hold_schema = load_schema("authority-resolution-hold.schema.json")

    def decision(self):
        return build_authority_hold_record(
            [{"representation_id": "R03", "input_type": "SRGB", "raw_value": [0, 166, 81]}],
            case_id="P02",
            evidence_refs=[{"record": "gate-4.json", "sha256": "a" * 64}],
            brand_owner_question="Which source controls?",
        )

    def test_unresolved_decision_validates(self):
        Draft202012Validator(self.decision_schema).validate(self.decision())

    def test_unresolved_decision_rejects_selected_representation(self):
        record = deepcopy(self.decision())
        record["selected_representation_id"] = "R03"
        self.assertFalse(Draft202012Validator(self.decision_schema).is_valid(record))

    def test_unresolved_decision_rejects_route_authorization(self):
        record = deepcopy(self.decision())
        record["route_authorization"] = "AUTHORIZED"
        self.assertFalse(Draft202012Validator(self.decision_schema).is_valid(record))

    def test_pre_binding_decision_rejects_atlas_id(self):
        record = deepcopy(self.decision())
        record["source_atlas_row_id"] = 5735
        self.assertFalse(Draft202012Validator(self.decision_schema).is_valid(record))

    def test_decision_rejects_candidate_metric_as_authority_selector(self):
        record = deepcopy(self.decision())
        record["selection_metrics_used"] = ["ATLAS_CANDIDATE"]
        self.assertFalse(Draft202012Validator(self.decision_schema).is_valid(record))

    def test_recognised_input_validates_without_selecting_authority(self):
        record = {
            "schema_id": "ATLAS_CLARUS_RECOGNISED_INPUT_RECORD_V0_1_0",
            "router_mode": "EXPERIMENTAL_SHADOW",
            "case_id": "P02",
            "representations": [{
                "representation_id": "R04", "input_type": "HEX", "raw_value": "#00A651",
                "source_identifier": None, "source_version": None, "source_sha256": None,
                "approval_reference": None, "provenance_status": "UNRESOLVED"
            }]
        }
        Draft202012Validator(self.input_schema).validate(record)

    def test_hold_schema_keeps_qc_not_measured(self):
        record = {
            "schema_id": "ATLAS_CLARUS_AUTHORITY_RESOLUTION_HOLD_V0_1_0",
            "router_mode": "EXPERIMENTAL_SHADOW", "case_id": "P02", "hold_status": "ACTIVE",
            "trigger_record": {"record": "gate-4.json", "sha256": "b" * 64, "condition": "SOURCE_AUTHORITY_UNRESOLVED"},
            "locked_actions": ["SOURCE_SELECTION", "ATLAS_ID_ASSIGNMENT", "IDENTITY_FREEZE", "PRODUCTION_ROUTING"],
            "permitted_actions": ["EVIDENCE_PRESERVATION", "BRAND_OWNER_REQUEST", "PROVENANCE_AUDIT"],
            "release_criteria": ["Controlling source and approval evidence are unambiguous."],
            "measured_qc_status": "NOT_MEASURED"
        }
        Draft202012Validator(self.hold_schema).validate(record)


if __name__ == "__main__":
    unittest.main()
