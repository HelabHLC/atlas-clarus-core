"""Experimental Source Authority contract for pre-binding control.

This module does not perform colour binding and does not select a source from
candidate results.  It provides an explicit guard that callers may place before
the normative v3.4.0 RGB binder.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence


AUTHORITY_ROUTER_MODE = "EXPERIMENTAL_SHADOW"
SOURCE_AUTHORITY_UNRESOLVED = "UNRESOLVED"
SOURCE_AUTHORITY_RESOLVED = "RESOLVED"
AUTHORITY_HOLD_ACTIVE = "ACTIVE"
AUTHORITY_HOLD_INACTIVE = "INACTIVE"
ROUTE_AUTHORIZED = "AUTHORIZED"
ROUTE_NOT_AUTHORIZED = "NOT_AUTHORIZED"
NOT_FROZEN_EXPERIMENTAL = "NOT_FROZEN_EXPERIMENTAL"


class AuthorityContractError(ValueError):
    """Raised when a Source Authority record violates the public contract."""


class AuthorityResolutionHold(AuthorityContractError):
    """Raised when normative binding is requested while authority is unresolved."""


def build_authority_hold_record(
    representations: Sequence[Mapping[str, Any]],
    *,
    case_id: str,
    evidence_refs: Sequence[Mapping[str, str]],
    brand_owner_question: str,
) -> dict[str, Any]:
    """Build an unresolved pre-binding hold without deriving colour identity.

    Representation values and evidence references are copied as supplied.  No
    distance, Lab, Delta E, ATLAS candidate, or production result is consulted.
    """
    if not case_id.strip():
        raise AuthorityContractError("case_id must not be empty")
    if not representations:
        raise AuthorityContractError("at least one representation is required")
    if not brand_owner_question.strip():
        raise AuthorityContractError("brand_owner_question must not be empty")

    ids = [item.get("representation_id") for item in representations]
    if any(not isinstance(item, str) or not item for item in ids):
        raise AuthorityContractError("every representation requires a non-empty representation_id")
    if len(ids) != len(set(ids)):
        raise AuthorityContractError("representation_id values must be unique")

    return {
        "schema_id": "ATLAS_CLARUS_SOURCE_AUTHORITY_DECISION_V0_1_0",
        "router_mode": AUTHORITY_ROUTER_MODE,
        "case_id": case_id,
        "representations": deepcopy(list(representations)),
        "evidence_refs": deepcopy(list(evidence_refs)),
        "source_authority": SOURCE_AUTHORITY_UNRESOLVED,
        "selected_representation_id": None,
        "authority_hold": AUTHORITY_HOLD_ACTIVE,
        "route_authorization": ROUTE_NOT_AUTHORIZED,
        "source_atlas_row_id": None,
        "source_atlas_display_row_number": None,
        "freeze_status": NOT_FROZEN_EXPERIMENTAL,
        "brand_owner_question": brand_owner_question,
        "selection_metrics_used": [],
        "measured_qc_status": "NOT_MEASURED",
    }


def assert_normative_binding_authorized(authority_record: Mapping[str, Any]) -> None:
    """Reject normative binding unless provenance has explicitly authorized it.

    This function intentionally does not call ``AtlasBinder``.  The existing
    binder remains unchanged and callers must invoke this guard before binding.
    """
    if authority_record.get("router_mode") != AUTHORITY_ROUTER_MODE:
        raise AuthorityContractError("unsupported Source Authority router mode")

    if authority_record.get("source_authority") != SOURCE_AUTHORITY_RESOLVED:
        raise AuthorityResolutionHold("source authority is unresolved")
    if authority_record.get("authority_hold") != AUTHORITY_HOLD_INACTIVE:
        raise AuthorityResolutionHold("authority-resolution hold is active")
    if authority_record.get("route_authorization") != ROUTE_AUTHORIZED:
        raise AuthorityResolutionHold("source route is not authorized")

    selected = authority_record.get("selected_representation_id")
    if not isinstance(selected, str) or not selected:
        raise AuthorityContractError("resolved authority requires selected_representation_id")

    evidence_refs = authority_record.get("evidence_refs")
    if not isinstance(evidence_refs, list) or not evidence_refs:
        raise AuthorityContractError("resolved authority requires evidence_refs")

    prohibited = {"DELTA_E", "RGB_DISTANCE", "ATLAS_CANDIDATE", "GAMUT", "DEVICE_VALUES"}
    metrics = authority_record.get("selection_metrics_used", [])
    if not isinstance(metrics, list):
        raise AuthorityContractError("selection_metrics_used must be an array")
    used = {str(metric).upper() for metric in metrics}
    if used.intersection(prohibited):
        raise AuthorityContractError("computed colour or production results cannot select source authority")

    # Source identity must still be absent before the existing binder runs.
    if authority_record.get("source_atlas_row_id") is not None:
        raise AuthorityContractError("pre-binding authority record must not assign source_atlas_row_id")
    if authority_record.get("source_atlas_display_row_number") is not None:
        raise AuthorityContractError("pre-binding authority record must not assign a display row number")

