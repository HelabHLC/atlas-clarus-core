# Canonical fixture matrix

`fixtures/canonical-binding-fixtures-v1.json` is the single machine-readable oracle for known binding results shared by the Core and application-integration evidence.

The public CI validates the matrix schema, verifies that every declared integration claim resolves to an existing manifest, and normalises the differently shaped Inkscape, GIMP, and Krita records before comparing their input RGB, frozen row ID, reference, master RGB, distance, and master SHA-256 with the canonical values.

This check proves that the published manifests agree on their recorded fixtures. It does not replace fresh execution in each application and does not upgrade runtime evidence to cross-system, device, or measured-QC evidence.
