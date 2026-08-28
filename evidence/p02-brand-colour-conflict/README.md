# P02 — Brand Colour Conflict Evidence Example

## Purpose

This package preserves Gates 1–5 of the synthetic **Northstar Green** case as a
reproducible example of the experimental/shadow Source Authority contract.

Six supplied representations claim to describe the same brand colour, but the
package contains no controlling Brand Owner approval or complete provenance that
would authorize any one representation as the source.

The example demonstrates a controlled unresolved outcome. It is not designed to
force a successful ATLAS identity assignment.

## Gate sequence

| Gate | Evidence purpose | Result |
| --- | --- | --- |
| 1 | Recognised Input and provenance audit | Six representations recognised; authority unresolved |
| 2 | Representation consistency | Conflict detected; no authority selected |
| 3 | Separate ATLAS candidate routes | Experimental/shadow divergence documented; no freeze |
| 4 | Formal Source Authority decision | No representation has sufficient authority evidence |
| 5 | Authority Resolution Hold | Identity and dependent production actions remain on hold |

## Reproducible terminal state

```text
SOURCE_AUTHORITY = UNRESOLVED
SELECTED_REPRESENTATION = null
source_atlas_row_id = null
source_atlas_display_row_number = null
FREEZE_STATUS = NOT_FROZEN_EXPERIMENTAL
AUTHORITY_RESOLUTION_HOLD = ACTIVE
production_processing = NOT_AUTHORIZED
measured_qc_status = NOT_MEASURED
```

## Critical interpretation

Gate 3 records three candidate identities across the comparable routes. Those
candidate results are challenge evidence only. Neither candidate agreement nor
the lowest colour distance is provenance, and neither may select Source
Authority.

This package therefore ends correctly without an ATLAS identity freeze.

## Integrity verification

From this directory:

```bash
sha256sum -c SHA256SUMS.txt
```

Repository CI additionally verifies:

- every manifest hash against the committed file bytes;
- exact gate order 1–5;
- uninterrupted `UNRESOLVED` and `NOT_FROZEN_EXPERIMENTAL` state;
- absence of a selected representation and frozen ATLAS row;
- non-binding Gate 3 candidate status;
- active Gate 5 authority hold;
- absence of production authorization and physical measured QC.

## Method boundary

The example does not change `src/atlas_clarus/binding.py`, does not add source
routes, does not freeze an identity, and does not implement 4C, ECG, ICC, device
values, production judgement, or measured QC.

Workflow v3.4.0 remains project-internally normative for documented 8-bit sRGB.
The Source Authority material remains `EXPERIMENTAL / SHADOW`.
