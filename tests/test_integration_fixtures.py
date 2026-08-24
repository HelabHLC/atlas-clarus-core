import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "fixtures" / "canonical-binding-fixtures-v1.json"
SCHEMA_PATH = ROOT / "schemas" / "canonical-fixture-matrix.schema.json"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


class IntegrationFixtureContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix = load_json(MATRIX_PATH)

    def test_canonical_matrix_validates(self):
        Draft202012Validator(load_json(SCHEMA_PATH)).validate(self.matrix)

    def test_every_integration_claim_resolves_to_a_fixture(self):
        fixture_ids = set(self.matrix["fixtures"])
        for integration, fixture_id in self.matrix["integration_claims"].items():
            with self.subTest(integration=integration):
                self.assertIn(fixture_id, fixture_ids)
                self.assertTrue((ROOT / "integrations" / integration / "MANIFEST.json").is_file())

    def test_integration_manifests_match_canonical_fixtures(self):
        for integration, fixture_id in self.matrix["integration_claims"].items():
            manifest = load_json(ROOT / "integrations" / integration / "MANIFEST.json")
            fixture = self.matrix["fixtures"][fixture_id]
            with self.subTest(integration=integration, fixture_id=fixture_id):
                self.assertEqual(self._master_hash(manifest), self.matrix["master_sha256"])
                observed = self._normalise_fixture(integration, manifest)
                self.assertEqual(observed, {
                    "input_rgb": fixture["input_rgb"],
                    "source_atlas_row_id": fixture["source_atlas_row_id"],
                    "source_reference": fixture["source_reference"],
                    "source_rgb": fixture["source_rgb"],
                    "source_rgb_distance_squared": fixture["source_rgb_distance_squared"],
                })

    @staticmethod
    def _master_hash(manifest):
        if "master" in manifest:
            return manifest["master"]["sha256"]
        return manifest["reference"]["upstream_master_sha256"]

    @staticmethod
    def _normalise_fixture(integration, manifest):
        if integration.startswith("inkscape/"):
            value = manifest["validated_fixture"]
            return {
                "input_rgb": [int(value["source_hex"][index:index + 2], 16) for index in (1, 3, 5)],
                "source_atlas_row_id": value["atlas_row_id"],
                "source_reference": value["reference"],
                "source_rgb": [int(value["pkl_hex"][index:index + 2], 16) for index in (1, 3, 5)],
                "source_rgb_distance_squared": value["d2_RGB"],
            }
        if integration.startswith("gimp/"):
            value = manifest["validated_fixture"]
            return {
                "input_rgb": value["source_rgb"],
                "source_atlas_row_id": value["source_atlas_row_id"],
                "source_reference": value["reference"],
                "source_rgb": value["pkl_rgb"],
                "source_rgb_distance_squared": value["d2_RGB"],
            }
        if integration.startswith("krita/"):
            value = manifest["validated_pixel"]
            return {
                "input_rgb": value["source_rgb"],
                "source_atlas_row_id": value["atlas_row_id"],
                "source_reference": value["reference"],
                "source_rgb": value["pkl_rgb"],
                "source_rgb_distance_squared": value["d2_RGB"],
            }
        raise AssertionError(f"No fixture adapter for {integration}")


if __name__ == "__main__":
    unittest.main()
