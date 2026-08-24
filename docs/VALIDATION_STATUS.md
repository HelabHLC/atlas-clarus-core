# Validation Status

**Date:** 2026-08-24  
**Technical baseline:** ATLAS Clarus Workflow v3.4.0  
**Master SHA-256:** `8283ab91b10f89ac758d09ecf5fb4d6343536600a06dd468b1cc1ecf4ec747c4`

## Status model

ATLAS Clarus separates evidence levels.

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

| Application | Source fixture | Runtime | Persistence / roundtrip | Cross-system | DEVICE | Measured QC |
|---|---|---|---|---|---|---|
| Inkscape | Documented | PASS reported for prototype | PASS reported | NOT EVIDENCED | NOT PROVIDED | NOT_MEASURED |
| GIMP | Supporting project evidence exists | PASS reported for GIMP 3.2.4 | NOT EVIDENCED | NOT EVIDENCED | NOT PROVIDED | NOT_MEASURED |
| Krita | Integration state reported | NOT EVIDENCED in current public package | NOT EVIDENCED | NOT EVIDENCED | NOT PROVIDED | NOT_MEASURED |

## Inkscape evidence note

The current project record includes an Inkscape v0.3.0 milestone reporting:

- extension execution PASS;
- CSS detection PASS;
- RGB-only binding PASS;
- HLC / PKL / row output PASS;
- audit metadata persistence PASS;
- saved SVG persistence PASS.

An earlier four-gate source-fixture manifest explicitly separated source-fixture success from runtime testing. This distinction should be preserved in the repository history.

## GIMP evidence note

A current project announcement records a GIMP 3.2.4 runtime pass and identifies deterministic `d²_RGB` matching and frozen source identity.

A machine-readable runtime manifest was not located in the current evidence set used to prepare this GitHub starter package.

Therefore the recommended public wording is:

> **Runtime pass reported — reproducibility package pending.**

## Krita evidence note

Krita is part of the current integration milestone, but a dedicated machine-readable runtime validation package was not located in the current evidence set used to prepare this GitHub starter package.

Therefore the recommended public wording is:

> **Integration present — dedicated validation package pending.**

## Physical measurement boundary

No application-integration evidence in this repository should be interpreted as physical print measurement.

Without physical measured data and project-specific limits:

```text
measured_qc_status = NOT_MEASURED
```
