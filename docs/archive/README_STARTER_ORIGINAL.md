# ATLAS Clarus Open Colour Project

**Status:** Public Beta / engineering project  
**Technical baseline:** ATLAS Clarus Workflow v3.4.0  
**Reference master:** `atlas_master__active_master__v2_illumext.pkl`  
**Master SHA-256:** `8283ab91b10f89ac758d09ecf5fb4d6343536600a06dd468b1cc1ecf4ec747c4`

ATLAS Clarus adds a documented colour-identity layer to open creative tools.

A source colour is assigned a stable reference identity **before** ICC conversion, device output or production assessment begins.

> **Identity first. Production feasibility second. Device values third. Measured QC last.**

## Current application milestone

ATLAS Clarus has now been exercised in multiple open creative applications:

| Application | Current public status | Evidence boundary |
|---|---|---|
| **Inkscape** | Validated prototype milestone | Real runtime / save-roundtrip evidence is documented for the v0.3.0 prototype. |
| **GIMP** | Runtime pass reported | Current evidence includes a GIMP 3.2.4 runtime-pass announcement; a machine-readable validation package should be published separately. |
| **Krita** | Integration present | Application use is part of the current project state; a dedicated validation package should be published before claiming an independently reproducible runtime pass. |

This is an **application-integration milestone**, not a claim of physical print validation, device qualification, external certification or production approval.

See [`docs/INTEGRATIONS.md`](docs/INTEGRATIONS.md) and [`docs/VALIDATION_STATUS.md`](docs/VALIDATION_STATUS.md).

## Core method

For documented 8-bit sRGB input, Workflow v3.4.0 binds the source to the active ATLAS master using:

```text
d²_RGB =
(Rs - Ri)² +
(Gs - Gi)² +
(Bs - Bi)²
```

Selection:

1. smallest integer `d²_RGB`;
2. exact tie → smaller `atlas_row_id`.

The selected `source_atlas_row_id` is frozen before downstream production analysis.

Lab, ΔE, Δλ, ICC, CMYK, gamut, substrate or device values must not retroactively redefine that frozen source identity.

## Architecture

```text
SOURCE
  ↓
REFERENCE IDENTITY
  ↓
FROZEN source_atlas_row_id
  ├──→ 4C feasibility
  ├──→ ECG / FOGRA55 feasibility
  ├──→ INTENT diagnostics
  ├──→ DEVICE values
  └──→ MEASURED QC
```

4C and ECG are parallel branches from the same frozen reference. ATLAS Clarus does **not** use a `4C → ECG` chain.

## What this project does not claim

ATLAS Clarus does not claim that:

- every source colour can be reproduced identically in every production condition;
- an RGB observation uniquely reconstructs a physical reflectance spectrum;
- PKL RGB is itself a measured spectral identity;
- a digital ICC result is a measured print result;
- ATLAS Clarus replaces ICC colour management;
- a runtime integration constitutes production approval;
- the project is certified or standardised by ISO, DIN, Fogra or another external body.

Workflow v3.4.0 is **project-internally normative**.

Without physical measurement:

```text
measured_qc_status = NOT_MEASURED
```

## Repository scope

This repository is intended to hold:

- project governance and method boundaries;
- open-tool integration notes;
- reproducible validation fixtures and manifests;
- application-specific installation packages where licensing permits;
- release notes, checksums and known limitations.

Reference datasets and executable components should only be added with verified provenance, licence information and checksums.

## Related project

The HelabHLC account also maintains `arbe-lambda`, a separate spectral-analysis project. ATLAS Clarus and ARBE λ* may exchange documented descriptors where appropriate, but they are not the same system and should remain separately versioned.

## Public Beta principle

External technical criticism and independent reproduction attempts are welcome.

If a result is not supported by a documented fixture, manifest, runtime record or physical measurement, it should be labelled accordingly rather than promoted to a stronger status.
