# Shadow Identity Baseline v0.3

Status: `FROZEN / PROJECT-INTERNAL NORMATIVE SHADOW IDENTITY`

Effective date: 2026-08-28

## Result

- 13,283 explicit and unique `atlas_row_id` values;
- 13,283 unique references;
- 13,283 unique v0.3 Frozen Identity digests;
- zero Python/Node digest mismatches;
- C01–C14 passed;
- aggregate digest invariant under physical table reordering;
- 13,283 verified v0.2 → v0.3 migration relations;
- zero migration holds.

Aggregate Identity SHA-256:

`e532055b834700000f3b2b7acf5768bbffc5071a87b9a25062f24b4f3a817989`

## Identity rule

The v0.3 digest binds:

```text
atlas_master_sha256
atlas_row_id
reference
binding_rule_version
master_version
reference_rgb
```

`cxf_object_index` is separate provenance and is not an identity substitute.

## Data notice

The Shadow Master is modified/derived machine-readable data. It is not the
unmodified freieFarbe source file.

Original HLC Colour Atlas XL data:
Copyright (c) freieFarbe e.V. — https://freiefarbe.de/

See [`../../../docs/LICENSE_AUDIT_HLC_ATLAS_XL.md`](../../../docs/LICENSE_AUDIT_HLC_ATLAS_XL.md)
and [`../../../THIRD_PARTY_NOTICES.md`](../../../THIRD_PARTY_NOTICES.md).

## Verification

```bash
node evidence/shadow-identity/v0.3/verify_migration_node.mjs \
  evidence/shadow-identity/v0.3/outputs/identity_digest_migration_v0_2_to_v0_3.csv \
  /tmp/node-migration-report.json

python -m unittest tests.test_shadow_identity_v03 -v
```

The active master and original CxF remain external hash-bound inputs and are
not committed.

