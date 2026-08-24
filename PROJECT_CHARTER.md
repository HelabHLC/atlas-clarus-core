# Project Charter

## Mission

ATLAS Clarus adds a documented colour-identity layer to open creative tools. A source colour is assigned a stable reference identity before ICC conversion, device output or production assessment begins.

## Problem

Creative applications commonly store colour coordinates and transform them between document and output spaces. That does not by itself provide a persistent, versioned answer to the question:

> Which documented reference colour was intended before production translation?

## Proposed contribution

ATLAS Clarus connects:

- deterministic RGB-only binding to a bound ATLAS master;
- a frozen `atlas_row_id` and the exact PKL RGB stored on that row;
- open HLC naming and available reference metadata;
- post-hoc Lab / ΔE comparison;
- optional ARBE / Δλ description where valid spectral data exist;
- parallel 4C and ECG feasibility;
- later DEVICE output and measured QC as separate evidence layers;
- integrations with open creative applications.

## Current application focus

The current Public Beta has practical integration work across:

- Inkscape;
- GIMP;
- Krita.

Application support does not by itself establish physical production validity.

## Initial audiences

### Education

- open and inspectable learning workflow;
- no mandatory proprietary creative-suite dependency;
- practical distinction between colour identity, production value and measurement;
- local or privacy-conscious deployment;
- reproducible exercises using open creative tools.

### Designers and start-ups

- versioned brand-colour registry;
- traceable hand-off to agencies and print providers;
- comparison of 4C and ECG production paths;
- evidence packages containing reference identity and production context.

### Prepress and production specialists

- preserved source identity;
- explicit ICC/profile context;
- separation of production feasibility from device values;
- measured QC only when physical measurement exists.

## Non-claims

The project does not claim that:

- an RGB observation uniquely reconstructs a physical reflectance spectrum;
- PKL RGB is itself a measured spectral identity;
- a digital ICC roundtrip proves physical print quality;
- ATLAS Clarus replaces ICC colour management;
- ARBE / Δλ has proven superiority without controlled validation;
- application integration equals external certification or production approval.

## Governance

- Workflow v3.4.0 is the active **project-internally normative** workflow.
- Normative rules change only through a recorded decision.
- Reference datasets remain immutable; derived files receive new versions.
- Every release should name workflow version, master hash, software versions and limitations.
- Experimental Source Authority routing remains separate unless formally promoted.
- Educational simplification must not remove scientific qualifications.
- Unsupported claims remain `OPEN QUESTION / NOT EVIDENCED`.

## Release principle

A feature is only described as validated at the level supported by its evidence.

Examples:

- source fixture pass;
- runtime pass;
- save-roundtrip pass;
- cross-system reproducibility;
- device qualification;
- measured QC.

These levels must not be collapsed into one generic "validated" label.
