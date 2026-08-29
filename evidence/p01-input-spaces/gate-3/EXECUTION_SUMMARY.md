# P01-A Gate-3 Freeze Verification Summary

**Status:** PASS  
**Freeze status:** FROZEN / VERIFIED  
**Scope:** Conformance and integrity only — no colour matching re-executed.

## Result

| Field | Verified value |
|---|---|
| Gate-2 selected `atlas_row_id` | 5082 |
| Persistent `source_atlas_row_id` | 5082 |
| Read-back `source_atlas_row_id` | 5082 |
| Reference | `H135_L070_C100` |
| ATLAS RGB | `[0, 200, 0]` |
| HEX | `#00C800` |
| `d²_RGB` | 3025 |
| Freeze record SHA-256 | `fc5c6432ea580739b98c6bc8a1a8ca5432867c5a2a218ac94bab81c52d3df967` |
| Canonical record SHA-256 | `aa0b8c3f2ea8391fc2760defde5e459a2189fd1a205575866608255babd41c9e` |

## Integrity proof

- Gate-2 predecessor SHA-256 verified.
- `src/atlas_clarus/binding.py` remained byte-identical at Git blob `52b5b5a9945e22fb1cd845e195b864b676288e99`.
- Gate-2 handoff `5082 → 5082` verified.
- Persistent JSON read-back returned `5082`.
- Attempted in-memory mutation of frozen `BindingResult.source_atlas_row_id` was blocked.
- A tampered persisted record (`5082 → 5081`) produced a digest mismatch and failed validation.
- A separate downstream `production_atlas_row_id` can differ without overwriting the source identity.

## CI evidence

- Tested commit: `4acfb0ac2462bf8d7be13acb9d9fbb257226caca`
- GitHub Actions CI run: `#61` / `33264747394`
- Overall conclusion: **success**
- Public contract: Python 3.10, 3.11, 3.12, 3.13 — **success**
- Real-master job: skipped; not required because Gate-3 does not re-run matching or load the master.

## Boundary

This evidence changes no colour-selection rule, no `binding.py`, no production logic, and no Gate-2 identity. It proves only that the already-selected identity was persisted and that mutation is detectable/rejected.

**Status transition justified:** `NOT_FROZEN_GATE2` → `FROZEN / VERIFIED`

**Publication state:** staged on branch `p01-gate3-freeze-evidence`; `main` remains unchanged.
