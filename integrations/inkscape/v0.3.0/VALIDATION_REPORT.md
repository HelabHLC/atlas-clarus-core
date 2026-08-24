# Validation report — Inkscape v0.3.0

The real-runtime smoke test bound one CSS stroke declaration:

`Source #00349C → HLC H285_L025_C065 → PKL #00379D → atlas_row_id 10519 | d²RGB = 10`

After Inkscape Save As, the returned SVG audit showed:

- active target `stroke:#00379D`: 1
- active source `stroke:#00349C`: 0
- extension: `0.3.0`
- method: `RGB_ONLY_INTEGER_D2`
- tie-break: `SMALLER_ATLAS_ROW_ID`
- K: `UNLIMITED`
- CSS records: 1

## Gate status

- `EXTENSION_EXECUTION = PASS`
- `CSS_DETECTION = PASS`
- `RGB_ONLY_BINDING = PASS`
- `HLC_PKL_ROW_OUTPUT = PASS`
- `AUDIT_METADATA_PERSISTENCE = PASS`
- `SAVED_SVG_PERSISTENCE = PASS`
- `INKSCAPE_RUNTIME = PASS`
- `MEASURED_QC = NOT_MEASURED`

The result validates the recorded fixture and save roundtrip. It does not establish universal compatibility or physical colour validation.
