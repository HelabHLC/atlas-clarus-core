# ATLAS Clarus Shadow Identity Baseline Decision v0.3

Decision status: `FROZEN`

Effective date: `2026-08-28`

Scope: `PROJECT-INTERNAL NORMATIVE / SHADOW IDENTITY`

## Decision

ATLAS Clarus Shadow Identity v0.3 is adopted as the project-internally
normative identity baseline for all new Shadow-lineage records.

The normative Frozen Reference Identity binds:

```text
atlas_master_sha256
atlas_row_id
reference
binding_rule_version
master_version
reference_rgb
```

The controlling active-master digest is:

`8283ab91b10f89ac758d09ecf5fb4d6343536600a06dd468b1cc1ecf4ec747c4`

The full 13,283-row aggregate identity digest is:

`e532055b834700000f3b2b7acf5768bbffc5071a87b9a25062f24b4f3a817989`

## Boundaries

- The active master is unchanged.
- Workflow v3.4.0 remains the active project-internal production baseline.
- v0.3 is normative for the Shadow Identity lineage only.
- Source Authority remains separately governed by its declared status.
- This decision is not external standards certification or physical QC.

## Supersession

Digest Rule v0.3 supersedes Digest Rule v0.2 for new Shadow records.

```text
SUPERSEDES_DIGEST_RULE_V0_2
```

Existing v0.2 records remain historically valid under their original rule and
must remain readable. They are not silently rewritten, deleted or relabelled.

## Change control

Any change to a normative field, canonicalization rule, bound master hash,
row-ID mapping or digest algorithm requires a new baseline version and a new
explicit decision record. Baseline v0.3 itself is immutable.

