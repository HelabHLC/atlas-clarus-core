# Validation Status

**Date:** 2026-08-24  
**Technical baseline:** ATLAS Clarus Workflow v3.4.0  
**Master SHA-256:** `8283ab91b10f89ac758d09ecf5fb4d6343536600a06dd468b1cc1ecf4ec747c4`

## Status model

```text
SOURCE_FIXTURE
→ APPLICATION_RUNTIME
→ SAVE / PERSISTENCE
→ CROSS-SYSTEM REPRODUCTION
→ DEVICE
→ MEASURED QC
```

A pass at one level does not imply a pass at the next level.

## Current evidence summary

| Application | Public package | Source fixture | Runtime | Persistence / roundtrip | Cross-system | DEVICE | Measured QC |
|---|---|---|---|---|---|---|---|
| Inkscape v0.3.0 | Published frozen baseline | Documented | PASS | PASS | NOT EVIDENCED | NOT PROVIDED | NOT_MEASURED |
| GIMP 3.2.4 | Pending | Supporting evidence exists | PASS reported | NOT EVIDENCED | NOT EVIDENCED | NOT PROVIDED | NOT_MEASURED |
| Krita v0.3.4 | Published frozen baseline | Documented | PASS | PASS evidence package | NOT EVIDENCED | NOT PROVIDED | NOT_MEASURED |

## Inkscape evidence note

The published [Inkscape v0.3.0 package](../integrations/inkscape/v0.3.0/) records extension execution, CSS detection, RGB-only binding, HLC/PKL/row output, audit metadata persistence and saved-SVG persistence as PASS.

Validated fixture:

`#00349C → H285_L025_C065 → #00379D → atlas_row_id 10519 → d²RGB 10`

The earlier four-gate source-fixture manifest remains separate from the real-runtime/save-roundtrip evidence.

## GIMP evidence note

A project announcement records a GIMP 3.2.4 runtime pass and deterministic `d²_RGB` binding with frozen source identity. A machine-readable runtime manifest and exact installable package have not yet been published.

Recommended public wording:

> **Runtime pass reported — reproducibility package pending.**

## Krita evidence note

The public [Krita v0.3.4 frozen package](../integrations/krita/v0.3.4/) records discovery, enablement, load, UI runtime, pixel capture, sampler cross-check, deterministic binding, source-identity freeze, 13,283-row full-master access and blank-search full-master behaviour as PASS.

## Physical measurement boundary

No application-integration evidence in this repository constitutes physical print measurement.

```text
measured_qc_status = NOT_MEASURED
```
