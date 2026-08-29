#!/usr/bin/env python3
"""P01-A Gate-3 source-identity freeze verifier.

This verifier does not rerun colour matching. It consumes the published Gate-2
selection as predecessor evidence and verifies persistence, read-back, in-memory
immutability, downstream source/production separation, and tamper detection.
"""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
from typing import Any

from atlas_clarus.binding import (
    BindingResult,
    EXPECTED_MASTER_SHA256,
    POSTHOC_MODE,
)

ROOT = Path(__file__).resolve().parents[3]
GATE2_PATH = ROOT / "evidence/p01-input-spaces/gate-2/P01-A_Gate-2_Full-Reference_Evidence_v0.1.json"
RECORD_PATH = ROOT / "evidence/p01-input-spaces/gate-3/P01-A_Gate-3_Source-Identity_Freeze_Record_v0.1.json"
EVIDENCE_PATH = ROOT / "evidence/p01-input-spaces/gate-3/P01-A_Gate-3_Freeze_Evidence_v0.1.json"
BINDING_PATH = ROOT / "src/atlas_clarus/binding.py"

EXPECTED_GATE2_SHA256 = "4e740f3c6d183f389e4c16ebb06461cc679acc84fba63c7084ad6cb53540dea1"
EXPECTED_GATE2_GIT_BLOB_SHA1 = "4a49cad0f386ea06d65b33361d61c223b4c425df"
EXPECTED_BINDING_GIT_BLOB_SHA1 = "52b5b5a9945e22fb1cd845e195b864b676288e99"
EXPECTED_RECORD_FILE_SHA256 = "fc5c6432ea580739b98c6bc8a1a8ca5432867c5a2a218ac94bab81c52d3df967"
EXPECTED_RECORD_CANONICAL_SHA256 = "aa0b8c3f2ea8391fc2760defde5e459a2189fd1a205575866608255babd41c9e"
EXPECTED_SOURCE_ATLAS_ROW_ID = 5082


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob_sha1(path: Path) -> str:
    payload = path.read_bytes()
    header = f"blob {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_freeze_record(record: dict[str, Any], gate2: dict[str, Any]) -> None:
    selected = gate2["selection"]["gate2_selected_atlas_row_id"]
    source_id = record["source_identity"]["source_atlas_row_id"]
    persistent_id = record["freeze"]["persistent_source_atlas_row_id"]
    readback_expected = record["freeze"]["readback_expected_source_atlas_row_id"]

    if selected != EXPECTED_SOURCE_ATLAS_ROW_ID:
        raise ValueError(f"Unexpected Gate-2 selected id: {selected}")
    if not (source_id == persistent_id == readback_expected == selected):
        raise ValueError(
            "Freeze chain mismatch: "
            f"gate2={selected}, source={source_id}, persistent={persistent_id}, "
            f"readback_expected={readback_expected}"
        )
    if record["source_identity"]["reference"] != "H135_L070_C100":
        raise ValueError("Reference mismatch")
    if record["source_identity"]["atlas_rgb"] != [0, 200, 0]:
        raise ValueError("ATLAS RGB mismatch")
    if record["source_identity"]["d2_rgb"] != 3025:
        raise ValueError("d2_RGB mismatch")
    if record["master_binding"]["sha256"] != EXPECTED_MASTER_SHA256:
        raise ValueError("Master SHA-256 mismatch")
    if record["freeze"]["freeze_status"] != "FROZEN":
        raise ValueError("Freeze record is not marked FROZEN")


def verify() -> dict[str, Any]:
    checks: dict[str, str] = {}

    def check(name: str, condition: bool) -> None:
        if not condition:
            raise AssertionError(name)
        checks[name] = "PASS"

    gate2 = load_json(GATE2_PATH)
    evidence = load_json(EVIDENCE_PATH)
    record = load_json(RECORD_PATH)

    check("gate2_predecessor_sha256", sha256_file(GATE2_PATH) == EXPECTED_GATE2_SHA256)
    check("gate2_predecessor_git_blob", git_blob_sha1(GATE2_PATH) == EXPECTED_GATE2_GIT_BLOB_SHA1)
    check("binding_core_blob_unchanged", git_blob_sha1(BINDING_PATH) == EXPECTED_BINDING_GIT_BLOB_SHA1)
    check("gate2_status", gate2["gate2_status"] == "PASS")
    check("gate2_freeze_boundary", gate2["gate_boundary"]["freeze_status"] == "NOT_FROZEN_GATE2")
    check("gate3_authorized", gate2["forward_contract"]["gate3_authorization"] == "READY")
    check(
        "gate2_selected_id",
        gate2["selection"]["gate2_selected_atlas_row_id"] == EXPECTED_SOURCE_ATLAS_ROW_ID,
    )

    check("freeze_record_file_hash", sha256_file(RECORD_PATH) == EXPECTED_RECORD_FILE_SHA256)
    check("freeze_record_canonical_hash", canonical_sha256(record) == EXPECTED_RECORD_CANONICAL_SHA256)
    check(
        "evidence_record_hash_binding",
        evidence["freeze_record"]["file_sha256"] == EXPECTED_RECORD_FILE_SHA256
        and evidence["freeze_record"]["canonical_sha256"] == EXPECTED_RECORD_CANONICAL_SHA256,
    )

    validate_freeze_record(record, gate2)
    check(
        "handoff_gate2_to_freeze",
        record["predecessor_binding"]["gate2_selected_atlas_row_id"]
        == record["freeze"]["persistent_source_atlas_row_id"]
        == EXPECTED_SOURCE_ATLAS_ROW_ID,
    )

    readback = load_json(RECORD_PATH)
    check(
        "persistent_readback",
        readback["freeze"]["persistent_source_atlas_row_id"] == EXPECTED_SOURCE_ATLAS_ROW_ID,
    )

    binding = BindingResult(
        input_rgb=(0, 255, 0),
        source_atlas_row_id=EXPECTED_SOURCE_ATLAS_ROW_ID,
        production_atlas_row_id=EXPECTED_SOURCE_ATLAS_ROW_ID,
        reference_variant=POSTHOC_MODE,
        source_rgb_distance_squared=3025,
        source_reference="H135_L070_C100",
        production_reference="H135_L070_C100",
        source_rgb=(0, 200, 0),
        production_rgb=(0, 200, 0),
        source_delta_lambda_nm=0.0,
        production_delta_lambda_nm=0.0,
        master_sha256=EXPECTED_MASTER_SHA256,
    )
    mutation_blocked = False
    try:
        binding.source_atlas_row_id = 5081
    except FrozenInstanceError:
        mutation_blocked = True
    check("binding_result_in_memory_mutation_blocked", mutation_blocked)
    check("binding_result_source_id_unchanged", binding.source_atlas_row_id == EXPECTED_SOURCE_ATLAS_ROW_ID)

    downstream = replace(
        binding,
        production_atlas_row_id=4886,
        production_reference="H130_L070_C105",
        production_rgb=(0, 199, 0),
    )
    check(
        "downstream_separate_production_id_preserves_source",
        downstream.source_atlas_row_id == EXPECTED_SOURCE_ATLAS_ROW_ID
        and downstream.production_atlas_row_id == 4886
        and binding.source_atlas_row_id == EXPECTED_SOURCE_ATLAS_ROW_ID,
    )

    tampered = copy.deepcopy(record)
    tampered["source_identity"]["source_atlas_row_id"] = 5081
    check("tampered_canonical_digest_detected", canonical_sha256(tampered) != EXPECTED_RECORD_CANONICAL_SHA256)

    tamper_rejected = False
    try:
        validate_freeze_record(tampered, gate2)
    except ValueError:
        tamper_rejected = True
    check("tampered_source_id_rejected", tamper_rejected)

    return {
        "status": "PASS",
        "program": "P01",
        "case_id": "P01-A",
        "gate": "GATE-3",
        "proof_scope": "SOURCE_IDENTITY_FREEZE_CONFORMANCE_AND_INTEGRITY",
        "colour_matching_reexecuted": False,
        "gate2_selected_atlas_row_id": EXPECTED_SOURCE_ATLAS_ROW_ID,
        "persisted_source_atlas_row_id": record["freeze"]["persistent_source_atlas_row_id"],
        "readback_source_atlas_row_id": readback["freeze"]["persistent_source_atlas_row_id"],
        "freeze_status": "FROZEN",
        "verification_status": "VERIFIED",
        "checks": checks,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
