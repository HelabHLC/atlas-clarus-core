# Known limitations — GIMP v0.1.3

- Runtime PASS is limited to the recorded GIMP 3.2.4 Windows fixture.
- The document-pixel route fails closed unless the image is RGB, U8 non-linear and its effective profile identifies as sRGB.
- The foreground procedure is a convenience route and does not establish document-pixel provenance.
- The plug-in performs reference matching; it does not evaluate production feasibility or generate device values.
- Lab, ΔE and ICC do not select source identity.
- `atlas_row_id` is the stable 0-based engineering binding of the hash-locked active master representation.
- Universal operating-system, GIMP-version, image-format and profile compatibility is not claimed.
- `measured_qc_status = NOT_MEASURED`.
