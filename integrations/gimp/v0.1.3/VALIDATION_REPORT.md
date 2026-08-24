# Validation report — GIMP v0.1.3

The recovered package was taken from the working GIMP user plug-ins directory and preserved byte-identically.

## Static gates

- ZIP integrity: PASS
- Python syntax: PASS
- plugin files complete: PASS
- bundled row count: 13,283 / PASS
- unique and sorted engineering `atlas_row_id`: PASS
- documented `#032802` regression: PASS

## Runtime gates

- GIMP 3.2.4 Windows menu registration: PASS
- RGB base-type gate: PASS
- U8 non-linear precision gate: PASS
- effective built-in sRGB profile gate: PASS
- merged document-pixel extraction at XY 548,1040: PASS
- deterministic full-master binding: PASS
- source identity freeze: PASS

Runtime result:

`#3D7B19 → H130_L045_C055 → row 4966 → #37791A → d²RGB 41 → FROZEN`

Independent recalculation against the exact bundled master reproduced every value: PASS.

This is a validated software prototype path, not physical colour measurement, device qualification, production approval or external certification.
