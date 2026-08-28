# Experimental Source Authority Contract v0.1.0

## Status and boundary

This contract is **EXPERIMENTAL / SHADOW**. It is a pre-binding control layer and
does not amend the project-internally normative ATLAS Clarus Workflow v3.4.0.
The deterministic RGB-only implementation in `binding.py` remains unchanged.

Core rule:

> Source provenance authorizes the route. Candidate results never select source authority.

## State sequence

```text
RECOGNISED INPUT
→ SOURCE AUTHORITY AUDIT
→ AUTHORITY HOLD or ROUTE AUTHORIZATION
→ existing source route
→ separate identity freeze
```

An unresolved authority decision must contain:

```text
source_authority = UNRESOLVED
selected_representation_id = null
authority_hold = ACTIVE
route_authorization = NOT_AUTHORIZED
source_atlas_row_id = null
source_atlas_display_row_number = null
freeze_status = NOT_FROZEN_EXPERIMENTAL
measured_qc_status = NOT_MEASURED
```

## Separation from binding

`atlas_clarus.authority.assert_normative_binding_authorized()` is an explicit
precondition guard. It does not call or modify `AtlasBinder`. A caller may invoke
the existing binder only after a provenance-backed authority record has:

- `source_authority = RESOLVED`;
- exactly one selected representation;
- `authority_hold = INACTIVE`;
- `route_authorization = AUTHORIZED`;
- at least one immutable evidence reference;
- no ATLAS identity assigned yet.

The ATLAS identity is created by the subsequently authorized source route, never
by this contract.

## Prohibited selectors

The following cannot establish source authority:

- Delta E;
- RGB distance;
- nearest ATLAS candidate;
- gamut result;
- device values;
- visual preference or an undocumented claim that representations are identical.

Experimental candidate comparisons may continue while a hold is active, but
must remain non-binding and cannot remove the hold.

## Schemas

- `recognised-input-record.schema.json` inventories representations without selection.
- `source-authority-decision.schema.json` expresses resolved or unresolved pre-binding state.
- `authority-resolution-hold.schema.json` records locked actions, permitted evidence work and release criteria.

## Out of scope

This first contract does not implement:

- Lab, spectral, RGB or other candidate routes;
- modifications to `binding.py`;
- identity freeze;
- 4C or ECG feasibility;
- ICC/device-value generation;
- production judgement;
- measured QC.
