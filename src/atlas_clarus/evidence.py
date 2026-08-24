"""Workflow v3.4.0 run-manifest construction and consistency checks."""

from __future__ import annotations

from collections import Counter
from typing import Any, Iterable, Mapping

from .binding import (
    ACTIVE_MODE,
    EXPECTED_MASTER_FILENAME,
    EXPECTED_MASTER_ROWS,
    EXPECTED_MASTER_SHA256,
    POSTHOC_MODE,
    BindingResult,
)

RUN_MANIFEST_SCHEMA_ID = "ATLAS_CLARUS_RUN_MANIFEST_V0_1_0"
WORKFLOW_VERSION = "3.4.0"
SHA256_LENGTH = 64

DEFAULT_LAYER_STATUS = {
    "runtime": "NOT_EVIDENCED",
    "persistence": "NOT_EVIDENCED",
    "cross_system": "NOT_EVIDENCED",
    "device": "NOT_PROVIDED",
    "measured_qc": "NOT_MEASURED",
}


class EvidenceContractError(ValueError):
    """Raised when records cannot form a coherent v3.4.0 run manifest."""


def _require_sha256(value: str, label: str) -> str:
    if len(value) != SHA256_LENGTH or any(character not in "0123456789abcdef" for character in value):
        raise EvidenceContractError(f"{label} must be a lowercase hexadecimal SHA-256")
    return value


def _operation(mode: str) -> dict[str, Any]:
    if mode == POSTHOC_MODE:
        return {
            "reference_variant": mode,
            "k": "UNLIMITED",
            "seed": 42,
            "delta_lambda_mode": "POSTHOC",
            "candidate_corridor": "SOURCE_ONLY",
            "candidate_count": 1,
            "production_reference_selection": "SOURCE_IDENTITY",
            "deltaE_in_selection": False,
        }
    if mode == ACTIVE_MODE:
        return {
            "reference_variant": mode,
            "k": "UNLIMITED",
            "seed": 42,
            "delta_lambda_mode": "ACTIVE",
            "candidate_corridor": "RGB_TOP_2",
            "candidate_count": 2,
            "production_reference_selection": "MIN_ABS_DELTA_LAMBDA_THEN_LOWER_ATLAS_ROW_ID",
            "deltaE_in_selection": False,
        }
    raise EvidenceContractError(f"Unsupported reference variant: {mode}")


def build_run_manifest(
    bindings: Iterable[BindingResult],
    *,
    input_sha256: str,
    software_name: str,
    software_version: str,
    runtime: str | None = None,
    platform: str | None = None,
    layer_status: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Build a complete run manifest from one result per processed pixel.

    Repeated bindings are collapsed in the atomic record list and counted in
    ``two_id_evidence.mapping``. All results must belong to one operating mode
    and the frozen v3.4.0 master.
    """

    results = tuple(bindings)
    if not results:
        raise EvidenceContractError("At least one binding result is required")
    if not software_name or not software_version:
        raise EvidenceContractError("Software name and version are required")
    _require_sha256(input_sha256, "input_sha256")

    modes = {result.reference_variant for result in results}
    if len(modes) != 1:
        raise EvidenceContractError("A run manifest cannot mix reference variants")
    mode = next(iter(modes))
    operation = _operation(mode)

    master_hashes = {result.master_sha256 for result in results}
    if master_hashes != {EXPECTED_MASTER_SHA256}:
        raise EvidenceContractError("All bindings must use the frozen v3.4.0 master SHA-256")

    if mode == POSTHOC_MODE and any(
        result.source_atlas_row_id != result.production_atlas_row_id for result in results
    ):
        raise EvidenceContractError("POSTHOC bindings must preserve source identity")

    record_by_key: dict[tuple[Any, ...], dict[str, Any]] = {}
    counts: Counter[tuple[Any, ...]] = Counter()
    result_by_key: dict[tuple[Any, ...], BindingResult] = {}
    for result in results:
        key = (
            result.input_rgb,
            result.source_atlas_row_id,
            result.production_atlas_row_id,
            result.source_rgb_distance_squared,
        )
        counts[key] += 1
        result_by_key[key] = result
        record_by_key[key] = result.to_record()

    total_pixels = len(results)
    mapping = []
    for key in sorted(counts, key=lambda item: (item[1], item[2], item[0])):
        result = result_by_key[key]
        production_changed = result.production_atlas_row_id != result.source_atlas_row_id
        mapping.append(
            {
                "source_atlas_row_id": result.source_atlas_row_id,
                "production_atlas_row_id": result.production_atlas_row_id,
                "pixel_count": counts[key],
                "pixel_fraction": counts[key] / total_pixels,
                "production_rgb_rank": 2 if production_changed else 1,
                "source_delta_lambda_nm": result.source_delta_lambda_nm,
                "production_delta_lambda_nm": result.production_delta_lambda_nm,
                "selection_reason": (
                    "MIN_ABS_DELTA_LAMBDA_WITHIN_RGB_TOP_2"
                    if mode == ACTIVE_MODE
                    else "SOURCE_IDENTITY"
                ),
            }
        )

    software = {"name": software_name, "version": software_version}
    if runtime:
        software["runtime"] = runtime
    if platform:
        software["platform"] = platform

    statuses = dict(DEFAULT_LAYER_STATUS)
    if layer_status:
        unknown = set(layer_status).difference(statuses)
        if unknown:
            raise EvidenceContractError(f"Unknown layer status fields: {', '.join(sorted(unknown))}")
        statuses.update(layer_status)

    return {
        "schema_id": RUN_MANIFEST_SCHEMA_ID,
        "workflow_version": WORKFLOW_VERSION,
        "software": software,
        "input": {"authority": "DOCUMENTED_8_BIT_SRGB", "sha256": input_sha256},
        "master": {
            "filename": EXPECTED_MASTER_FILENAME,
            "sha256": EXPECTED_MASTER_SHA256,
            "row_count": EXPECTED_MASTER_ROWS,
        },
        "operation": operation,
        "bindings": [record_by_key[key] for key in sorted(record_by_key, key=lambda item: (item[1], item[2], item[0]))],
        "two_id_evidence": {"total_pixels": total_pixels, "mapping": mapping},
        "layer_status": statuses,
    }
