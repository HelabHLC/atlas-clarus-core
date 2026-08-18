# ATLAS Clarus Workflow v3.4.0

## RGB-only with two mandatorily separated Δλ operating modes

**Version:** 3.4.0  
**Status:** Approved / normative  
**Release date:** 2026-08-03  
**Supersedes:** ATLAS Clarus Workflow v3.3.0  
**Removed from the active normative package:** ATLAS Clarus Workflow v2.1.1  
**Master binding:** `atlas_master__active_master__v2_illumext.pkl`  
**Master SHA-256:** `8283ab91b10f89ac758d09ecf5fb4d6343536600a06dd468b1cc1ecf4ec747c4`

---

## 1. Purpose

This workflow mandatorily separates:

1. the deterministic RGB-only source identity;
2. the possible active Δλ production selection;
3. ICC output;
4. downstream measurement and comparative evaluation.

The central rule is:

```text
source_atlas_row_id
=
unchanged RGB-only source identity

production_atlas_row_id
=
production reference optionally determined by Δλ
```

The `source_atlas_row_id` must never be overwritten.

---

## 2. Mandatory process chains

### Operating mode A — Δλ post-hoc

```text
Original pixel
→ RGB-only Full Reference
→ source_atlas_row_id
→ Δλ description
→ optional ICC
→ Production Output
→ optional Measured QC
```

In this operating mode:

```text
production_atlas_row_id = source_atlas_row_id
```

### Operating mode B — active Δλ production selection

```text
Original pixel
→ RGB-only Full Reference
→ freeze source_atlas_row_id
→ RGB_TOP_2 candidate corridor
→ selection by minimum |Δλ|
→ production_atlas_row_id
→ optional ICC
→ Production Output
→ optional Measured QC
```

The active operating mode may determine a different `production_atlas_row_id`.  
The `source_atlas_row_id` remains unchanged as the provenance record.

---

## 3. Mandatory operating modes

Permitted values:

```text
RGB_ONLY_DLambda_POSTHOC
RGB_ONLY_DLambda_ACTIVE_PRODUCTION_SELECTION
```

Unless explicitly specified, the default is:

```text
RGB_ONLY_DLambda_POSTHOC
```

A silent or retrospective change of operating mode is prohibited.

---

## 4. RGB-only source identity

For a source pixel `s = (Rs, Gs, Bs)` and a valid Atlas row `i = (Ri, Gi, Bi)`:

```text
d²_RGB(s,i)
=
(Rs - Ri)²
+
(Gs - Gi)²
+
(Bs - Bi)²
```

The `source_atlas_row_id` is determined by:

```text
argmin_i (
    d²_RGB(s,i),
    atlas_row_id_i
)
```

Sort key:

1. smallest integer squared RGB distance;
2. in the event of a tie, the smaller `atlas_row_id`.

Prohibited influences on source identity:

- CIELAB;
- ΔE76;
- ΔE94;
- CMC;
- CIEDE2000;
- HLC distance;
- Δλ;
- ICC;
- CMYK;
- GamutMap;
- material or profile approval.

---

## 5. Meaning of K = UNLIMITED

```text
K = UNLIMITED
```

means:

- no reduction of the image to a fixed colour palette;
- every pixel is referenced against the complete valid Atlas;
- the number of Atlas identities used is determined by the image.

`K = UNLIMITED` is **not** identical to the number of candidates used by active Δλ selection.

The normative active Δλ operating mode separately requires:

```text
candidate_corridor = RGB_TOP_2
candidate_count = 2
```

---

## 6. Operating mode A — Δλ post-hoc

Manifest value:

```json
{
  "reference_variant": "RGB_ONLY_DLambda_POSTHOC",
  "delta_lambda_mode": "POSTHOC",
  "candidate_corridor": null,
  "candidate_count": 0,
  "production_reference_selection": "SOURCE_IDENTITY_PRESERVED",
  "deltaE_in_selection": false
}
```

Δλ is read and documented after the source identity has been frozen.

Required metrics:

- `lambda_v2_nm`;
- `lambda_ee_nm`;
- `delta_lambda_nm`;
- mean signed Δλ;
- median signed Δλ;
- mean `|Δλ|`;
- median `|Δλ|`;
- P95 of `|Δλ|`;
- maximum `|Δλ|`.

In this operating mode, Δλ has an exclusively descriptive function.

---

## 7. Operating mode B — active Δλ production selection

Manifest value:

```json
{
  "reference_variant": "RGB_ONLY_DLambda_ACTIVE_PRODUCTION_SELECTION",
  "delta_lambda_mode": "ACTIVE_PRODUCTION_SELECTION",
  "candidate_corridor": "RGB_TOP_2",
  "candidate_count": 2,
  "production_reference_selection": "MINIMUM_ABS_DELTA_LAMBDA",
  "deltaE_in_selection": false
}
```

### 7.1 Candidate generation

For every original pixel, the two nearest valid Atlas rows in RGB are determined.

Sorting:

```text
1. d²_RGB ascending
2. atlas_row_id ascending
```

Candidate generation takes place exclusively in the documented 8-bit sRGB space.

### 7.2 Selection rule

For every candidate:

```text
|Δλ|
=
abs(delta_lambda_nm)
=
abs(lambda_v2_nm - lambda_ee_nm)
```

The production reference is determined by:

```text
production_atlas_row_id
=
argmin_c (
    abs(delta_lambda_nm_c),
    atlas_row_id_c
)
```

where `c` originates exclusively from `RGB_TOP_2`.

### 7.3 Hard rules

- ΔE does not influence candidate generation.
- ΔE does not influence selection.
- ΔE is not a weight.
- ΔE is not a switching condition.
- ΔE is not a tie-break.
- Lab is not a selection metric.
- The `source_atlas_row_id` is not replaced.
- The `production_atlas_row_id` is stored separately.
- The Δλ step may be performed without ICC.
- If ICC output is generated later, the `production_atlas_row_id` is the production input.

---

## 8. Role of Delta E

In both operating modes, Delta E may be calculated only **after selection has been completed and frozen**.

Permitted purposes:

- comparing the original with the source reference;
- comparing the original with the production reference;
- comparing the source reference with the production reference;
- comparing ICC variants;
- evaluating physically measured production.

Required declaration:

```json
{
  "deltaE_stage": "POSTHOC_ONLY",
  "deltaE_influenced_source_identity": false,
  "deltaE_influenced_production_selection": false
}
```

A downstream improvement or deterioration in ΔE is a measurement result.  
It is not part of the Δλ selection rule.

---

## 9. Two-ID evidence

When active Δλ selection is used, at least the following must be stored:

- `source_atlas_row_id.npy`;
- `production_atlas_row_id.npy`;
- `source_to_production_mapping.csv`;
- source and production reference;
- pixel count and pixel share;
- RGB rank of the production reference;
- source Δλ;
- production Δλ;
- `|Δλ|` of both references;
- reason for selection;
- tie-break rule;
- Atlas version;
- master hash;
- image hash.

The two ID layers must not be merged into a single column.

---

## 10. ICC production output and parallel production evaluation

ICC is a downstream production stage.

### Post-hoc mode

```text
source_atlas_row_id
├── conventional 4C ICC evaluation
└── FOGRA55 ECG ICC evaluation
```

### Active mode

```text
production_atlas_row_id
├── conventional 4C ICC evaluation
└── FOGRA55 ECG ICC evaluation
```

Conventional 4C and FOGRA55 ECG are independent, parallel production paths. Neither path is derived from the other. Results from one path must not be used as the input values for the other path.

ICC must not modify either `source_atlas_row_id` or `production_atlas_row_id`.

For each production path, the following must be recorded separately:

- production-path identifier;
- ICC profile name;
- ICC profile hash;
- rendering intent;
- black-point-compensation setting;
- output colour space;
- target material or printing condition;
- generated device values;
- software and version;
- digital feasibility or comparison result;
- measured QC result, when physical measurements are available.

A digital ICC calculation is not a measured print result.

---

## 11. Out-of-gamut and GamutMap

GamutMap remains an analysis and control view.

Out-of-gamut references are not removed from the evidence record.

```text
source_atlas_row_id remains preserved
production_atlas_row_id remains preserved
each ICC production path generates its own printable device value
```

A change of profile or material generates new device values, not automatically new Atlas identities.

---

## 12. Measured QC

Without physical measurement:

```text
measured_qc_status = NOT_MEASURED
```

Permitted states:

```text
NOT_MEASURED
MEASURED_NO_LIMITS
PASS
WATCH
REVIEW
BLOCK
```

For `PASS`, `WATCH`, `REVIEW`, or `BLOCK`, project-specific limits and measurement conditions are required.

When conventional 4C and FOGRA55 ECG are evaluated in parallel, each path requires its own `measured_qc_status` and its own measurement record.

---

## 13. Mandatory gates

```text
Gate 0   Validate and hash master
Gate 1   Document RGB input space
Gate 2   Execute RGB-only Full Reference
Gate 3   Freeze source_atlas_row_id
Gate 4   Verify Δλ operating mode
Gate 5A  POSTHOC: describe Δλ
Gate 5B  ACTIVE: generate RGB_TOP_2 and select production_atlas_row_id
Gate 6   Calculate optional post-hoc metrics
Gate 7   Optionally determine Profile Feasibility independently for each production path
Gate 8   Optionally generate ICC Production Output independently for 4C and FOGRA55 ECG
Gate 9   Execute Measured QC separately for each production path or document NOT_MEASURED
Gate 10  Verify package, colour, and hash integrity
Release  Approve or block
```

No gate may retrospectively overwrite the `source_atlas_row_id`.

---

## 14. Standard parameters

```text
RGB basis                     = documented 8-bit sRGB
RGB distance                  = integer squared Euclidean distance
K                             = UNLIMITED
Default mode                  = Δλ POSTHOC
Active Δλ corridor            = RGB_TOP_2
Active Δλ selection           = minimum |delta_lambda_nm|
Tie-break                     = smaller atlas_row_id
Seed                          = 42 documented, not used
Delta E in selection          = no
Lab in selection              = no
ICC in selection              = no
Production evaluation         = parallel, path-specific
Conventional production path  = 4C
Extended-gamut path           = FOGRA55 ECG
```

---

## 15. Result report

Every report separates:

### Measurement

IDs, hashes, reference changes, Δλ metrics, optional ΔE metrics, profiles, and device values.

For parallel 4C and FOGRA55 ECG evaluation, profile metadata, device values, feasibility results, and measured QC must be reported separately for each path.

### Interpretation

Classification of reference stability, the effect of active Δλ, and the output of each production path.

### Decision

Approval, observation, review, or blocking with justification. Production-path decisions must remain separately attributable.

### Limitations

Limits of RGB-only processing, the candidate corridor, Δλ selection, ICC preview, extended-gamut evaluation, and physical measurement.

---

## 16. Mandatory communication rule

Permitted:

> ATLAS Clarus may use Δλ either as a downstream analytical metric or as an active production selection within a documented RGB candidate corridor.

Permitted:

> The source identity remains preserved; active Δλ selection may determine a separate production reference.

Permitted:

> Conventional 4C and FOGRA55 ECG are evaluated as independent, parallel production paths from the same frozen ATLAS identity.

Not permitted:

- “Δλ is always exclusively descriptive.”
- “Δλ guarantees a smaller ΔE deviation.”
- “RGB_TOP_2 is optimal for every image.”
- “An ICC preview is already a measured print result.”
- “The production reference replaces the provenance record.”
- “FOGRA55 ECG is derived sequentially from the conventional 4C result.”
- “The result of one production path represents measured QC for the other path.”

---

## 17. Test evidence and scope of validity

The documented no-ICC comparison showed:

- `RGB_TOP_2` changed approximately 42% of pixel assignments;
- `RGB_TOP_12` changed approximately 95% of pixel assignments;
- the change occurred without ΔE involvement in selection.

This demonstrates that `|Δλ|` has an operative selection function in the active operating mode.

The test does not prove that every Δλ selection improves colour proximity.  
Therefore, `RGB_TOP_2` is the normative reproducible reference, while larger candidate corridors must be identified as experimental.

The documented comparison does not by itself validate conventional 4C or FOGRA55 ECG production. Each production path requires its own profile-bound calculation and, where claimed, its own physical measurement evidence.

---

## 18. Version and legacy rule

With the release of v3.4.0:

```text
v3.4.0 = sole active normative version
v3.3.0 = superseded
v2.1.1 = removed from the active normative package
```

Historical runs remain unchanged and must retain their original workflow version.

A recalculation is always performed with a new run ID and an explicitly documented Δλ operating mode.
