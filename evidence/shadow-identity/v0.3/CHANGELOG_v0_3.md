# ATLAS Clarus Shadow Identity v0.3 Changelog

## Added

- explicit immutable `atlas_row_id`;
- mandatory `reference` in the Frozen Identity payload;
- three-part binding invariant: master hash + row ID + reference;
- separate `cxf_object_index` provenance field;
- reorder-invariant aggregate identity digest;
- v0.2-to-v0.3 migration mapping;
- negative tests for row-ID/reference mutation and CxF-index substitution.

## Preserved

- all 13,283 ATLAS reference identities;
- active-master bytes and SHA-256;
- RGB binding rule v3.4.0;
- profile and production-target invariance;
- `NOT_MEASURED` QC boundary;
- historical readability of v0.2 digests.

## Changed

Frozen Identity digests intentionally change because the normative payload is
stronger. v0.3 digests supersede rather than overwrite v0.2 digests.

