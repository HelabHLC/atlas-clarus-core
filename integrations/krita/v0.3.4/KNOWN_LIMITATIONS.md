# Known Limitations — ATLAS Clarus × Krita v0.3.4

- Validation covers the tested Krita v0.3.4 runtime path, not every Krita version/platform/document type.
- Direct source authority in the validated path is `Document.pixelData`; the real-canvas sampler is only an independent cross-check.
- Identity selection is RGB-only under the documented workflow; downstream Δλ does not redefine frozen source identity.
- The full-master UI gate establishes access to 13,283 rows; it does not independently validate every row semantically.
- Physical colour, print and instrument QC were not performed: `MEASURED_QC = NOT_MEASURED`.
- This is a validated prototype baseline, not a certification or production approval.
- The frozen v0.3.4 files must not be silently modified. Future changes require a new version and regression testing.
