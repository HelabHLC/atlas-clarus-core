from copy import deepcopy
import unittest

from atlas_clarus import (
    AuthorityContractError,
    AuthorityResolutionHold,
    assert_normative_binding_authorized,
    build_authority_hold_record,
)


QUESTION = "Which supplied representation is the controlling source, and what evidence proves its authority?"


class SourceAuthorityContractTests(unittest.TestCase):
    def setUp(self):
        self.representations = [
            {"representation_id": "R01", "input_type": "CIELAB", "raw_value": [61, -55, 40]},
            {"representation_id": "R03", "input_type": "SRGB", "raw_value": [0, 166, 81]},
        ]
        self.hold = build_authority_hold_record(
            self.representations,
            case_id="P02",
            evidence_refs=[{"record": "gate-4.json", "sha256": "a" * 64}],
            brand_owner_question=QUESTION,
        )

    def test_unresolved_authority_creates_pre_binding_hold(self):
        self.assertEqual(self.hold["source_authority"], "UNRESOLVED")
        self.assertEqual(self.hold["authority_hold"], "ACTIVE")
        self.assertEqual(self.hold["route_authorization"], "NOT_AUTHORIZED")
        self.assertIsNone(self.hold["source_atlas_row_id"])
        self.assertIsNone(self.hold["source_atlas_display_row_number"])
        self.assertEqual(self.hold["freeze_status"], "NOT_FROZEN_EXPERIMENTAL")

    def test_unresolved_authority_blocks_normative_binding(self):
        with self.assertRaises(AuthorityResolutionHold):
            assert_normative_binding_authorized(self.hold)

    def test_candidate_result_cannot_remove_hold(self):
        challenged = deepcopy(self.hold)
        challenged["candidate_results"] = {"R03": {"atlas_row_id": 5735, "distance": 2.23}}
        challenged["source_authority"] = "RESOLVED"
        challenged["selected_representation_id"] = "R03"
        challenged["authority_hold"] = "INACTIVE"
        challenged["route_authorization"] = "AUTHORIZED"
        challenged["selection_metrics_used"] = ["ATLAS_CANDIDATE"]
        with self.assertRaises(AuthorityContractError):
            assert_normative_binding_authorized(challenged)

    def test_resolved_provenance_can_authorize_route_before_binding(self):
        resolved = deepcopy(self.hold)
        resolved["source_authority"] = "RESOLVED"
        resolved["selected_representation_id"] = "R03"
        resolved["authority_hold"] = "INACTIVE"
        resolved["route_authorization"] = "AUTHORIZED"
        resolved["selection_metrics_used"] = []
        assert_normative_binding_authorized(resolved)
        self.assertIsNone(resolved["source_atlas_row_id"])

    def test_pre_binding_authority_record_must_not_contain_atlas_id(self):
        resolved = deepcopy(self.hold)
        resolved.update({
            "source_authority": "RESOLVED",
            "selected_representation_id": "R03",
            "authority_hold": "INACTIVE",
            "route_authorization": "AUTHORIZED",
            "source_atlas_row_id": 5735,
        })
        with self.assertRaises(AuthorityContractError):
            assert_normative_binding_authorized(resolved)

    def test_duplicate_representation_ids_are_rejected(self):
        duplicate = [self.representations[0], self.representations[0]]
        with self.assertRaises(AuthorityContractError):
            build_authority_hold_record(
                duplicate, case_id="P02", evidence_refs=[], brand_owner_question=QUESTION
            )


if __name__ == "__main__":
    unittest.main()
