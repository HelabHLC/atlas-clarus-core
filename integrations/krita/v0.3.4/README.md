# ATLAS Clarus × Krita v0.3.4

**Release class:** Validated Prototype Baseline  
**Freeze status:** FROZEN  
**Workflow:** ATLAS Clarus Workflow v3.4.0  
**Measured QC:** NOT_MEASURED

This directory publishes the byte-identical frozen Krita integration and its reproducibility record.

## User download

Download [`ATLAS_Clarus_Krita_v0_3_4_FULL_MASTER_SEARCH.zip`](ATLAS_Clarus_Krita_v0_3_4_FULL_MASTER_SEARCH.zip) for installation in Krita.

SHA-256:

`a702a1125bfa4a86cb7eb8d7ba09155c33d0e49b21bf3ec55eaa45ce9625ed29`

The complete evidence archive is available as [`ATLAS_Clarus_Krita_v0.3.4_VALIDATED_PROTOTYPE_FREEZE.zip`](ATLAS_Clarus_Krita_v0.3.4_VALIDATED_PROTOTYPE_FREEZE.zip).

SHA-256:

`8254f5f6872e00540b1162de08ce78c81e0a4635cad19304decd79e8ac9d65f0`

## Installation

See [`INSTALL.md`](INSTALL.md).

## Validated path

```text
Canvas click
→ Document.pixelData
→ documented 8-bit sRGB
→ deterministic full-master PKL lookup
→ HLC / atlas_row_id
→ source identity FREEZE
```

Validated fixture:

```text
XY 659,479
→ RGB 242,226,214 / #F2E2D6
→ H050_L090_C010
→ atlas_row_id 1660
→ PKL RGB 243,223,212 / #F3DFD4
→ d²_RGB 14
→ FROZEN
```

The tested runtime gates, evidence boundary and limitations are recorded in [`MANIFEST.json`](MANIFEST.json), [`VALIDATION_REPORT.md`](VALIDATION_REPORT.md) and [`KNOWN_LIMITATIONS.md`](KNOWN_LIMITATIONS.md).

## Licence boundary

- ATLAS Clarus software code: MIT License; see the repository root `LICENSE`.
- Bundled HLC colour-reference data: attributed separately in `THIRD_PARTY_DATA_NOTICE.md`; it is not relicensed under MIT.
- Krita is a separate KDE project and is not distributed by this repository.

This is a validated prototype baseline, not physical measurement, device qualification, external certification or production approval.
