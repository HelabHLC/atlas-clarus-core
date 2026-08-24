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

### Core real-master gate

The hash-bound Core suite was executed against the authoritative 9,741,473-byte PKL master on commit `885979347b95633c5ccb4995be6b526ec3e541a6`.

`23 tests run → 23 passed → 0 failed → 0 skipped`

This includes the canonical four-case POSTHOC matrix and the ACTIVE two-ID regression. The machine-readable record is published under [`evidence/real-master/`](../evidence/real-master/). This Core PASS does not alter the application, cross-system, DEVICE, or measured-QC statuses below.

| Application | Public package | Source fixture | Runtime | Persistence / roundtrip | Cross-system | DEVICE | Measured QC |
|---|---|---|---|---|---|---|---|
| Inkscape v0.3.0 | Published frozen baseline | Documented | PASS | PASS | NOT EVIDENCED | NOT PROVIDED | NOT_MEASURED |
| GIMP 3.2.4 / plug-in v0.1.3 | Published frozen baseline | Documented | PASS | Runtime record published | NOT EVIDENCED | NOT PROVIDED | NOT_MEASURED |
| Krita v0.3.4 | Published frozen baseline | Documented | PASS | PASS evidence package | NOT EVIDENCED | NOT PROVIDED | NOT_MEASURED |

## Inkscape evidence note

The published [Inkscape v0.3.0 package](../integrations/inkscape/v0.3.0/) records extension execution, CSS detection, RGB-only binding, HLC/PKL/row output, audit metadata persistence and saved-SVG persistence as PASS.

Validated fixture:

`#00349C → H285_L025_C065 → #00379D → atlas_row_id 10519 → d²RGB 10`

The earlier four-gate source-fixture manifest remains separate from the real-runtime/save-roundtrip evidence.

## GIMP evidence note

The published [GIMP v0.1.3 frozen package](../integrations/gimp/v0.1.3/) preserves the recovered original plugin and records the GIMP 3.2.4 Windows document-pixel runtime pass:

`XY 548,1040 → #3D7B19 → H130_L045_C055 → row 4966 → #37791A → d²RGB 41 → FROZEN`

Independent recalculation against the exact bundled 13,283-row master reproduced every value: PASS.

## Krita evidence note

The public [Krita v0.3.4 frozen package](../integrations/krita/v0.3.4/) records discovery, enablement, load, UI runtime, pixel capture, sampler cross-check, deterministic binding, source-identity freeze, 13,283-row full-master access and blank-search full-master behaviour as PASS.

## Physical measurement boundary

No application-integration evidence in this repository constitutes physical print measurement.

```text
measured_qc_status = NOT_MEASURED
```
