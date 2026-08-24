# Known limitations — Inkscape v0.3.0

- Validated scope is the tested SVG/CSS `#RRGGBB` fill/stroke path.
- Gradient-stop colours are not bound by v0.3.0.
- Embedded raster pixels are not modified.
- Opacity is not modified.
- Named colours, `rgb()`, `rgba()`, CSS variables and advanced cascade cases are not validated.
- Direct object binding requires selection; document-level CSS is handled separately.
- Lab, ΔE and ICC do not select source identity.
- Runtime PASS does not cover every Inkscape version, platform, SVG feature, renderer or export format.
- Physical print behaviour and measured QC were not tested.
- The compact bundled reference is preserved as release data and is governed separately from MIT software code.
