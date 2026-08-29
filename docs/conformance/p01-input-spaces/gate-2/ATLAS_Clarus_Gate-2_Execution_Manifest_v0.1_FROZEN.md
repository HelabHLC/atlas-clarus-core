# ATLAS Clarus — P01 Gate-2 Execution Manifest v0.1

**Status:** `FROZEN`  
**Program:** `P01`  
**Gate:** `GATE-2 / RGB_ONLY_FULL_REFERENCE`  
**Freeze date:** `2026-08-29`  
**Normative JSON SHA-256:** `ae866f5484eed44b0dc6b7283c81b577b39aaa8be483b3e5375adb9c96839256`

## Authorized route

Only **P01-A** is authorized to enter Gate-2.

Input: sRGB `0,255,0`  
Route: `NORMATIVE`

P01-B and P01-C remain SHADOW and are not executed in Gate-2.

## Frozen master

- `atlas_master__active_master__v2_illumext.pkl`
- SHA-256 `8283ab91b10f89ac758d09ecf5fb4d6343536600a06dd468b1cc1ecf4ec747c4`
- 13,283 rows
- internal `atlas_row_id = DataFrame index`
- display row = `atlas_row_id + 1`

## Selection

Every valid master row is evaluated.

`d²_RGB = (Rs-Ri)² + (Gs-Gi)² + (Bs-Bi)²`

Sort key:

1. `d²_RGB` ascending
2. `atlas_row_id` ascending

No Lab, Delta E, Delta Lambda, ICC, CMYK, gamut mapping, material or profile approval may influence selection.

## Gate boundary

Gate-2 selects `gate2_selected_atlas_row_id`.

It does **not** persistently freeze `source_atlas_row_id`.  
That is reserved for Gate-3.

Gate-2 PASS authorizes Gate-3 to freeze the selected row.
