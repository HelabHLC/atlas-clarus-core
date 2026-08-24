# Application Integrations

## Scope

ATLAS Clarus is being connected to open creative applications so that a source colour can be bound to a documented ATLAS reference before production translation.

The applications do not define the reference identity themselves. They provide a user-facing environment around the same documented reference logic.

## Shared reference rule

For documented 8-bit sRGB:

```text
SOURCE RGB
→ integer squared RGB distance
→ smaller atlas_row_id on exact tie
→ freeze source_atlas_row_id
```

Downstream ICC, CMYK, gamut, substrate and device operations must not rewrite the frozen identity.

## Inkscape

**Current status:** validated prototype milestone.

Documented evidence currently supports:

- extension execution;
- CSS colour detection;
- RGB-only binding;
- HLC / PKL / `atlas_row_id` output;
- audit metadata persistence;
- saved SVG persistence / roundtrip.

The documented prototype milestone is v0.3.0.

This is a software/runtime validation level only.

```text
measured_qc_status = NOT_MEASURED
```

## GIMP

**Current status:** runtime pass reported.

The current project evidence identifies:

- GIMP 3.2.4;
- deterministic `d²_RGB` matching;
- frozen source identity;
- runtime pass.

Before calling this independently reproducible, publish:

1. the exact integration package;
2. source fixture(s);
3. expected ATLAS binding(s);
4. runtime log or machine-readable manifest;
5. package SHA-256;
6. application version and platform;
7. limitations.

## Krita

**Current status:** validated prototype baseline v0.3.4; frozen installation and evidence package published.

The frozen v0.3.4 package is published at [`integrations/krita/v0.3.4/`](../integrations/krita/v0.3.4/). It includes the installable plugin ZIP, manifest, checksums, validation report and known limitations.

The recorded gates apply to the tested runtime path. The exact Krita application version and universal platform compatibility were not captured in the frozen manifest.

## Terminology

Prefer:

- `integration present`
- `source fixture pass`
- `runtime pass`
- `save-roundtrip pass`
- `cross-system reproduced`

Avoid using the single word `validated` without naming the level.

None of these terms means:

- device qualification;
- measured print conformance;
- production approval;
- external certification.
