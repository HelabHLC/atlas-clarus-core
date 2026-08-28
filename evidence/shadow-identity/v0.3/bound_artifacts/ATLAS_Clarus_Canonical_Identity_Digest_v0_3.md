# ATLAS Clarus Canonical Identity Digest v0.3

Status: `PROJECT-INTERNAL NORMATIVE / SHADOW LINEAGE`

## Normative payload

Exactly these fields belong to the Frozen Reference Identity payload:

1. `atlas_master_sha256`
2. `atlas_row_id`
3. `binding_rule_version`
4. `master_version`
5. `reference`
6. `reference_rgb`

Canonical JSON uses UTF-8 without BOM, lexicographically sorted object keys,
no insignificant whitespace, JSON integers for IDs and channels, and lowercase
hexadecimal SHA-256.

```text
identity_digest_v0_3 = lowercase_hex(
  SHA-256(UTF-8(canonical_json(normative_payload)))
)
```

`cxf_object_index`, timestamps, run IDs, paths, implementation metadata,
production targets, profiles and QC results are excluded.

An aggregate master-identity digest SHALL serialize the per-row tuples
`atlas_row_id|reference|identity_digest` in ascending numeric `atlas_row_id`
order. It is therefore invariant under physical table reordering.

## Binding invariant

Before freezing, the implementation SHALL prove that
`atlas_master_sha256 + atlas_row_id + reference` resolves to exactly one row in
the bound master. Missing fields, mismatches or substitution of
`cxf_object_index` SHALL produce `E_IDENTITY_BINDING_ERROR`.

## Migration

v0.3 intentionally produces new identity digests. A v0.2 digest SHALL NOT be
silently relabelled as v0.3. Migration records SHALL preserve both digests and
state `SUPERSEDES_DIGEST_RULE_V0_2`.
