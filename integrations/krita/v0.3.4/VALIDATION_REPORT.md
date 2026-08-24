# ATLAS Clarus × Krita v0.3.4 — Validation Report

**Release class:** VALIDATED PROTOTYPE BASELINE  
**Freeze status:** FROZEN  
**Workflow:** ATLAS Clarus Workflow v3.4.0

## Runtime evidence

The plugin was discovered, enabled and loaded in Krita as **ATLAS Clarus PKL · Engineering Beta v0.3.4**.

Validated direct pixel path:

`Canvas click → Document.pixelData → 8-bit sRGB → deterministic PKL lookup → HLC / atlas_row_id → FREEZE`

Validated test pixel:

`XY 659,479 → RGB 242,226,214 / #F2E2D6 → H050_L090_C010 → atlas_row_id 1660 → PKL RGB 243,223,212 / #F3DFD4 → d²_RGB 14 → FROZEN`

The independent real-canvas sampler cross-check returned the same source RGB and the UI reported **RAW/SAMPLER CROSSCHECK = PASS**.

## Full-master gate

The UI reported **Full PKL master: 13283 rows**. With the search query blank, the full master remained available, establishing the v0.3.4 full-master-search gate.

## PASS gates

- KRITA_PLUGIN_DISCOVERY = PASS
- KRITA_PLUGIN_ENABLED = PASS
- KRITA_PLUGIN_LOAD = PASS
- ATLAS_CLARUS_UI_RUNTIME = PASS
- CANVAS_CLICK_CAPTURE = PASS
- DOCUMENT_PIXELDATA_READ = PASS
- CANVAS_SAMPLER_CROSSCHECK = PASS
- RGB_ONLY_PKL_BINDING = PASS
- SOURCE_IDENTITY_FREEZE = PASS
- FULL_MASTER_13283 = PASS
- SEARCH_SCOPE = FULL_MASTER
- FULL_MASTER_UI_ACCESS = PASS
- BLANK_SEARCH_RETURNS = ALL_MASTER_ROWS = PASS
- MEASURED_QC = NOT_MEASURED

This freeze is the regression baseline for future Krita development.
