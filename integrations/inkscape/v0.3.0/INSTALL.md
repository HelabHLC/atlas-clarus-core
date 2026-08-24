# Installation — ATLAS Clarus × Inkscape v0.3.0

## Requirements

- Inkscape with Python-based `inkex` extensions enabled.
- Write access to the Inkscape user extensions directory.
- A backup copy of every SVG used for testing.

The frozen evidence establishes the recorded runtime path only. It does not claim compatibility with every Inkscape version or operating system.

## Install

1. Download `ATLAS_Clarus_Inkscape_v0.3.0_VALIDATED_PROTOTYPE_FREEZE.zip`.
2. Verify its SHA-256 against `SHA256SUMS.txt`.
3. Extract the outer freeze archive.
4. Open `01_EXTENSION/ATLAS_Clarus_Inkscape_v0_3_0.zip`.
5. Extract the folder `atlas-clarus-inkscape-v0.3.0` into the Inkscape user extensions directory.
6. In Inkscape, locate that directory under **Edit → Preferences → System → User extensions**.
7. Remove or disable older ATLAS Clarus v0.2.x folders.
8. Restart Inkscape.

## Use

1. Open an SVG and save a working copy.
2. Select objects when binding direct `fill` or `stroke` values.
3. Run **Extensions → Color → ATLAS Clarus · Bind Colours v0.3.0**.
4. Review the reported Source → HLC → PKL → `atlas_row_id` records.
5. Save as a new SVG so the audit metadata and original remain separable.

Document-level CSS `<style>` declarations are processed separately and do not require an object selection.

## Verify removal

To uninstall, close Inkscape, remove the single folder `atlas-clarus-inkscape-v0.3.0` from the user extensions directory, and restart Inkscape.
