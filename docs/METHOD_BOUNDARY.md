# Method Boundary

## Active baseline

ATLAS Clarus Workflow v3.4.0 remains the active **project-internally normative** technical workflow.

The Source Authority Router is experimental and defaults to shadow/comparison use.

## Mandatory separation

```text
Reference Identity
→ Production Feasibility
→ Device Values
→ Measured QC
```

## Identity freeze

For documented 8-bit sRGB, source identity is selected by minimum integer squared RGB distance with smaller `atlas_row_id` as exact tie-break.

Once selected:

```text
source_atlas_row_id = FROZEN
```

Lab, ΔE, Δλ, ICC, CMYK, gamut, substrate and device conditions do not retroactively change that identity.

## Production branches

4C and ECG / FOGRA55 are parallel branches:

```text
FROZEN ATLAS REFERENCE ──→ 4C
                       └──→ ECG / FOGRA55
```

Never:

```text
4C → ECG
```

## QC

Without physical measurement:

```text
measured_qc_status = NOT_MEASURED
```

Do not assign production approval solely from digital analysis.
