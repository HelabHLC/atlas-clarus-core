# Application Integrations

## Scope

ATLAS Clarus connects to open creative applications so that a documented 8-bit sRGB source can be bound to an ATLAS reference before production translation.

The applications provide a user-facing environment around the same reference logic; they do not redefine the reference identity.

## Shared reference rule

```text
SOURCE RGB
→ integer squared RGB distance
→ smaller atlas_row_id on exact tie
→ freeze source_atlas_row_id
```

Downstream ICC, CMYK, gamut, substrate and device operations must not rewrite the frozen identity.

## Inkscape

**Current status:** installable frozen validated-prototype baseline v0.3.0.

The public package is available at [`integrations/inkscape/v0.3.0/`](../integrations/inkscape/v0.3.0/) with the byte-identical freeze archive, installation instructions, manifest, validation report, limitations, licence boundary and checksum.

Recorded gates:

- extension execution;
- CSS colour detection;
- RGB-only binding;
- HLC / PKL / `atlas_row_id` output;
- audit metadata persistence;
- saved-SVG persistence / Inkscape save roundtrip.

The PASS scope is the recorded SVG/CSS `#RRGGBB` fixture, not every Inkscape colour mechanism, version, platform or output path.

```text
measured_qc_status = NOT_MEASURED
```

## GIMP

**Current status:** installable frozen validated-prototype baseline v0.1.3.

The public package is available at [`integrations/gimp/v0.1.3/`](../integrations/gimp/v0.1.3/) with the recovered original plugin, runtime record, independent recalculation, installation instructions, manifest, limitations, licence boundary and checksums.

Recorded GIMP 3.2.4 Windows document-pixel fixture:

`XY 548,1040 → #3D7B19 → H130_L045_C055 → row 4966 → #37791A → d²RGB 41 → FROZEN`

PASS is limited to the recorded RGB/U8 non-linear/built-in-sRGB runtime path.

## Krita

**Current status:** installable frozen validated-prototype baseline v0.3.4.

The public package is available at [`integrations/krita/v0.3.4/`](../integrations/krita/v0.3.4/) with installable plugin, manifest, checksums, validation report and limitations.

## Terminology

Prefer evidence-specific labels such as `source fixture pass`, `runtime pass`, `save-roundtrip pass` and `cross-system reproduced`.

None of these terms means device qualification, measured print conformance, production approval or external certification.
