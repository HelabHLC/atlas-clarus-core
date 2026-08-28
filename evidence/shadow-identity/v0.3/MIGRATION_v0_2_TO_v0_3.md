# Migration: Frozen Identity Digest v0.2 → v0.3

Status: `APPROVED FOR SHADOW LINEAGE`

## Why migration is required

Digest v0.2 contained `source_atlas_row_id` but did not bind the textual
`reference`. It also did not express the now-explicit Shadow Master
`atlas_row_id` contract.

Digest v0.3 binds both row ID and reference to the exact master hash. A row-ID /
reference mismatch therefore becomes detectable before freezing.

## Migration relation

Migration creates a new v0.3 digest and preserves the old v0.2 digest:

```text
old_identity_digest_v0_2
    --SUPERSEDED_BY-->
new_identity_digest_v0_3
```

This is not an in-place update.

## Required migration record

Each migrated identity contains:

- active-master SHA-256;
- explicit `atlas_row_id`;
- exact `reference`;
- old v0.2 digest;
- new v0.3 digest;
- relation `SUPERSEDED_BY`;
- reason `EXPLICIT_ROW_ID_AND_REFERENCE_BINDING`;
- migration status `MIGRATED_VERIFIED`.

## Read rules

- Readers SHALL accept a v0.2 record only as `LEGACY_READ_ONLY`.
- New freezes SHALL use v0.3.
- A v0.2 digest SHALL never be compared directly with a v0.3 digest as though
  they used the same payload.
- Equivalence across versions SHALL be established through the supplied
  migration mapping and the common master/row/reference binding.
- Missing or ambiguous mappings SHALL produce `MIGRATION_HOLD`.

## Rollback

Rollback means returning new Shadow writes to `HOLD`; it does not delete v0.3
records or rewrite them as v0.2. The immutable migration table remains audit
evidence.

