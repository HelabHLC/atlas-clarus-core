# Roadmap

## Phase 0 — Foundation

- [x] Establish project charter.
- [x] Freeze initial scope and non-claims.
- [x] Establish project-internal normative baseline at Workflow v3.4.0.
- [ ] Publish a verified source-file and licence inventory.
- [ ] Publish checksums for all redistributed reference and integration packages.

## Phase 1 — Open creative-tool integration

- [x] Demonstrate deterministic RGB-only reference binding in an Inkscape prototype.
- [x] Document an Inkscape v0.3.0 runtime/save-roundtrip milestone.
- [x] Record a GIMP 3.2.4 runtime-pass milestone.
- [x] Establish Krita as part of the current application-integration scope.
- [ ] Publish one machine-readable validation manifest per application.
- [ ] Publish reproducible installation instructions per application.
- [ ] Validate the same reference fixtures on a second independent system.

## Phase 2 — Shared integration contract

- [ ] Define a common input contract for 8-bit sRGB / HEX.
- [ ] Standardise application output fields:
  - `source_rgb`
  - `source_atlas_row_id`
  - ATLAS/HLC reference
  - master RGB / HEX
  - `d²_RGB`
  - workflow version
  - master hash
- [ ] Define persistence requirements for each application.
- [ ] Define application-specific limitations without altering reference identity.

## Phase 3 — Production feasibility

- [ ] Maintain independent 4C branch.
- [ ] Maintain independent FOGRA55 ECG branch.
- [ ] Record ICC name, SHA-256, rendering intent and BPC.
- [ ] Keep digital feasibility, DEVICE and measured QC visibly separate.
- [ ] Validate deterministic output on a second system.

## Phase 4 — Education and public beta

- [ ] Create guided colour-identity lessons using open creative tools.
- [ ] Publish minimal reproducible test files.
- [ ] Add external reviewer instructions.
- [ ] Invite independent reproduction and issue reports.
- [ ] Track disagreements and failed tests as first-class evidence.

## Phase 5 — Source Authority research

- [ ] Keep Source Authority Router experimental / shadow by default.
- [ ] Compare exact ATLAS/HLC, sRGB, Lab and spectral source representations.
- [ ] Do not promote a spectral binding rule until deterministic method and metadata requirements are defined.
- [ ] Preserve v3.4.0 results separately from experimental routes.

## Release gate

No phase is described as validated beyond the evidence actually published.

A runtime pass is not measured QC.  
A digital ICC result is not physical production approval.
