# ATLAS Clarus Core

ATLAS Clarus Core is the development repository for a deterministic and traceable colour-reference identity system.

## Core principle

> Colour identity first. Production translation second.

ATLAS Clarus separates three layers that must not be confused:

1. **Reference identity** — a persistent and documented ATLAS reference.
2. **Colour transformation** — profile- and intent-dependent ICC/PCS processing.
3. **Device output and quality control** — production values and measured verification.

A production conversion may change RGB, CMYK, or other device values. It must not silently replace the underlying reference identity.

## Parallel production evaluation

A frozen ATLAS reference identity may be evaluated independently against conventional 4C and FOGRA55 ECG production conditions. These are parallel, profile-dependent production paths. Neither path modifies the underlying ATLAS reference identity, and neither path is derived from the other.

Each path produces and records its own:

- target profile and profile hash;
- rendering intent and black-point-compensation setting;
- device values;
- digital feasibility or comparison result;
- measured quality-control result, when physical measurements are available.

The architecture is therefore:

```text
Frozen ATLAS reference identity
├── 4C evaluation          ──> separate result ──> separate measured QC
└── FOGRA55 ECG evaluation ──> separate result ──> separate measured QC
```

A digital ICC calculation must not be presented as a measured print result.

## Current status

This repository is private and under active development. It is intended to contain the verified binding core, schemas, tests, technical documentation, and integration adapters.

The current work is a reference implementation. It is not a replacement for physical measurement, professional colour-management software, production proofing, or measured quality control.

## Methodological boundaries

- Reference identity and device recipes are stored separately.
- 4C and FOGRA55 ECG are independent, parallel production evaluations.
- ICC profiles, rendering intent, and black-point compensation belong to the production layer.
- Runtime derivatives must not be treated as independent colour authorities.
- Master assets require explicit provenance and cryptographic verification.
- Results described as digital calculations must not be presented as measured print results.

## Planned repository structure

```text
src/          Core implementation
tests/        Deterministic and regression tests
schemas/      Machine-readable record definitions
docs/         Methodology and architecture
adapters/     Application integrations
examples/     Reproducible, non-normative examples
```

## Related repository

The existing trace and viewer implementation remains separate:

- [atlas-clarus-trace-live](https://github.com/HelabHLC/atlas-clarus-trace-live)

## Confidentiality

This repository is private. Do not commit credentials, customer profiles, licensed datasets, unpublished master files, or unverified exports.
