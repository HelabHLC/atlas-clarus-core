# ATLAS Clarus — P01-A Gate-2 RGB-only Full-Reference Execution v0.1

**Gate-2 status:** `PASS`  
**Publication status:** `PUBLICATION READY`  
**Freeze status:** `NOT_FROZEN_GATE2`  
**Gate-3 authorization:** `READY`

## Input and frozen master

- Input: sRGB `[0,255,0]`
- Master rows evaluated: `13,283 / 13,283`
- Master SHA-256: `8283ab91b10f89ac758d09ecf5fb4d6343536600a06dd468b1cc1ecf4ec747c4`
- P01-A Gate-1 predecessor SHA-256: `e7d4b87ca6274e2d15edcc975591e682c62bff3fe0ad04f90020cc846b9a8dbc`
- Frozen Gate-2 manifest SHA-256: `ae866f5484eed44b0dc6b7283c81b577b39aaa8be483b3e5375adb9c96839256`

## Deterministic winner

- `gate2_selected_atlas_row_id = 5082`
- display row = `5083`
- reference = `H135_L070_C100`
- ATLAS RGB = `[0,200,0]`
- HEX = `#00C800`
- `d²_RGB = 3025`
- winner tie count = `1`

## Runner-up tie diagnostic

- deterministic runner-up = `4886`
- runner-up `d²_RGB = 3136`
- `runner_up_tie_count = 2`
- tied row IDs = `[4886, 5081]`
- tie-break = smaller `atlas_row_id`, therefore `4886`

## Verification

The independent verifier v0.3.0:

- hashes the actual published P01-A Gate-1 predecessor;
- validates the frozen master before pickle deserialization;
- executes two independent full 13,283-row RGB rankings;
- validates all Gate-2 Evidence and boundary fields;
- verifies `VERIFICATION_REPORT.json`;
- validates `PACKAGE_MANIFEST.json`;
- validates the eight-file payload scope in `SHA256SUMS.txt`.

`SHA256SUMS.txt` does not include itself; this avoids self-reference while still
hash-binding every other package payload artifact, including
`VERIFICATION_REPORT.json`.

## Gate boundary

Gate-2 remains `NOT_FROZEN_GATE2`.

Gate-3 authorization: `READY`, but Gate-3 has **not** been executed here.
No persistent `source_atlas_row_id` has yet been written by this package.

`gate2_selected_atlas_row_id` remains a **P01 conformance-harness staging field**.
It does not replace or amend Workflow v3.4.0 or `src/atlas_clarus/binding.py`.

No Lab, Delta E, Delta Lambda, ICC, CMYK, gamut mapping, material approval,
profile approval or measured physical QC influenced Gate-2.
