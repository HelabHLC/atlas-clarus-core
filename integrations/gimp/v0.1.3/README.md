# ATLAS Clarus × GIMP v0.1.3 — Frozen Release Package

**Release class:** `VALIDATED_PROTOTYPE_BASELINE`  
**Freeze status:** `FROZEN`  
**Runtime:** GIMP 3.2.4 on Windows  
**Workflow basis:** ATLAS Clarus v3.4.0  
**Measured QC:** `NOT_MEASURED`

This archive freezes the recovered, actually installed ATLAS Clarus GIMP Engineering Beta v0.1.3 package and its recorded document-pixel runtime pass.

## Validated document-pixel path

`XY 548,1040 → #3D7B19 → H130_L045_C055 → row 4966 → #37791A → d²RGB 41 → FROZEN`

The result was independently recalculated against the exact bundled 13,283-row reference and matched every reported field.

## Contents

- `01_ORIGINAL_PLUGIN/` — byte-identical ZIP recovered from the working GIMP installation
- `02_RUNTIME_EVIDENCE/` — operator-returned runtime record and independent recalculation
- `03_DOCUMENTATION/` — installation, validation report, limitations and licence/data boundary
- `MANIFEST.json` — machine-readable release metadata
- `SHA256SUMS.txt` — SHA-256 inventory

Do not silently modify v0.1.3. Future development belongs to a new version and must be regression-tested against this baseline.
824954e620ad0ed715a466c271c810eeb878530c
