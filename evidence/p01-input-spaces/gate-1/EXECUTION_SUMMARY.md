# ATLAS Clarus — P01 Gate-1 Execution Evidence v0.1

**Execution timestamp:** `2026-08-29T12:51:06Z`  
**Frozen Gate-1 manifest SHA-256:** `7a887316eac2aa1959459c4a6339502bf324ff3c2213a6e26650fac03bb061bf`  
**Independent verifier:** `verify_p01_gate1_reference.py` (`4063c68491347aef6f076822b529c004e703948aa241ec6773ca43ec634ebcdb`)  
**Scope:** Source-input validation and native-whitepoint colorimetric reconstruction only.

## Results

| Case | Declared input | Route | Reconstructed XYZ | White | Gate-1 | Forward state |
|---|---|---|---|---|---|---|
| P01-A | sRGB `0,255,0` | NORMATIVE | `0.3576, 0.7152, 0.1192` | D65 | **PASS** | Gate-2 authorized |
| P01-B | Adobe RGB (1998) `0,255,0` | SHADOW | `0.18556, 0.62736, 0.07069` | D65 | **PASS** | Shadow only; no identity freeze |
| P01-C | ROMM RGB `0,255,0` | SHADOW | `0.1352, 0.7118, 0.0000` | D50 | **PASS** | Shadow only; no identity freeze |

## Independent method

The verifier uses only the Python standard library. For each source RGB encoding it embeds the normative primaries, white point, inverse transfer function, and source reference. It derives the RGB-to-XYZ matrix independently from primaries + white point at runtime; the evidence XYZ values are not used to build the verification matrix.

Run from the repository/package context:

```bash
python verify_p01_gate1_reference.py --manifest /path/to/ATLAS_Clarus_Gate-1_Execution_Manifest_v0.1_FROZEN.json
```

## Gamut-status semantics

`IN_DECLARED_SOURCE_RGB_GAMUT` means only that the supplied uint8 triplet lies inside the declared source-encoding range. It is **not** evidence of destination, ICC-output, device, print, or production gamut.

## Gate-1 boundary

No ATLAS/PKL matching, `source_atlas_row_id`, Delta E, Delta Lambda, identity freeze, production conversion, ICC output, or physical measured QC is performed.

`measured_qc_status = NOT_MEASURED`
