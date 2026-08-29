# ATLAS Clarus — Gate‑1 Execution Manifest v0.1

**Manifest ID:** `ATLAS-CLARUS-GATE1-EXECUTION-MANIFEST`  
**Gate:** `GATE-1 / INPUT_SPACES`  
**Program:** `P01`  
**Status:** `FROZEN`  
**Freeze date:** `2026-08-29`  
**Normative artifact:** `ATLAS_Clarus_Gate-1_Execution_Manifest_v0.1_FROZEN.json`  
**Normative SHA-256:** `7a887316eac2aa1959459c4a6339502bf324ff3c2213a6e26650fac03bb061bf`

## 1. Zweck

Gate‑1 validiert und rekonstruiert den **deklarierten RGB-Eingaberaum deterministisch**, bevor irgendeine ATLAS-Referenzzuordnung stattfindet.

Gate‑1 ist damit ausschließlich ein **Input-/Rekonstruktions-Gate**. Es vergibt **keine ATLAS-Identität**.

## 2. Eingefrorene P01-Routen

| Case | Input | Route | Gate‑2-Freigabe | Identity Freeze in Gate‑1 |
|---|---|---|---|---|
| P01-A | sRGB `0,255,0` | NORMATIVE | ja, nach PASS | verboten |
| P01-B | Adobe RGB (1998) `0,255,0` | SHADOW | nein | verboten |
| P01-C | ROMM RGB `0,255,0` | SHADOW | nein | verboten |

**Festlegung:** P01-B und P01-C bleiben auch bei `PASS` reine Shadow-/Challenger-Routen. Ein Gate‑1-PASS autorisiert dort keinen Freeze.

## 3. Input Contract

Pflichtfelder:
- `case_id`
- `input_space`
- `rgb_u8`
- `input_space_authority`
- `conversion_path_id`

RGB-Eingabe:
- 3 Kanäle
- Reihenfolge `RGB`
- Datentyp `uint8`
- Wertebereich `0..255`

Deklarierte Weißpunkte:
- sRGB → D65
- Adobe RGB (1998) → D65
- ROMM RGB → D50

**Verboten:** implizites Erraten oder Ersetzen des Farbraums.

## 4. Normative Ausführungsreihenfolge

1. `G1.0_VALIDATE_MANIFEST_INTEGRITY`
2. `G1.1_VALIDATE_CASE_AND_CHANNEL_ENCODING`
3. `G1.2_VALIDATE_DECLARED_INPUT_SPACE`
4. `G1.3_RESOLVE_CANONICAL_CONVERSION_PATH`
5. `G1.4_RECONSTRUCT_COLORIMETRIC_STATE`
6. `G1.5_RECORD_GAMUT_AND_CLIP_DIAGNOSTICS`
7. `G1.6_EMIT_GATE1_EVIDENCE`
8. `G1.7_DECIDE_GATE1_STATUS`

Die Reihenfolge ist eingefroren.

## 5. Harte Gate‑1-Regeln

Innerhalb von Gate‑1 sind verboten:
- implizites Color-Space-Guessing;
- Pre-Conversion-Clipping;
- ATLAS Matching;
- ΔE;
- Δλ;
- Vergabe von `source_atlas_row_id`;
- PKL Match;
- Identity Freeze;
- Produktions- oder QC-Aussagen.

ROMM RGB wird als deklarierter **D50**-Quellraum behandelt; sRGB und Adobe RGB (1998) als deklarierte **D65**-Quellräume.

## 6. Required Evidence

Jede Ausführung muss mindestens protokollieren:
- `case_id`
- `input_space`
- `rgb_u8`
- `input_space_authority`
- `conversion_path_id`
- `conversion_path_version`
- `reconstructed_colorimetric_state`
- `gamut_status`
- `clip_status`
- `gate1_status`
- `diagnostics`
- `execution_timestamp`

Fehlt ein Pflichtnachweis, ist `PASS` unzulässig.

## 7. Status-Semantik

**PASS**  
Input-Encoding und deklarierter Farbraum sind gültig; der kanonische Conversion Path ist verfügbar; die Rekonstruktion wurde abgeschlossen; alle Pflichtnachweise wurden erzeugt.

**FAIL**  
Input ist ungültig oder mehrdeutig, der deklarierte Farbraum kann nicht aufgelöst werden, die Rekonstruktion scheitert oder Pflichtnachweise fehlen.

**NOT_EXECUTED**  
Der Case wurde nicht ausgeführt. Aus diesem Status darf keine technische Aussage abgeleitet werden.

## 8. Gate-Grenze

Gate‑1 darf ausschließlich bestätigen:
- Inputraum erkannt;
- Encoding gültig;
- kanonischer Conversion Path ausgeführt;
- colorimetrischer Zustand rekonstruiert;
- Gamut-/Clip-Diagnostik protokolliert.

Gate‑1 darf **nicht** bestätigen:
- ATLAS Identity;
- `atlas_row_id`;
- PKL Match;
- ΔE oder Δλ;
- Produktionsfähigkeit;
- ICC-Output;
- gemessene QC.

## 9. Forward Contract

- **P01-A:** `PASS` → darf in **Gate‑2 RGB-only Full-Reference** übergehen.
- **P01-B:** `PASS` → bleibt **SHADOW**; nur colorimetrische Challenger-Route; kein Freeze.
- **P01-C:** `PASS` → bleibt **SHADOW**; nur colorimetrische Challenger-Route; kein Freeze.

## 10. Sperre / Freeze

**FROZEN bedeutet:**
- alle Manifestfelder sind gesperrt;
- In-place-Änderungen sind verboten;
- Backports in v0.1 sind verboten;
- jede semantische oder byteweise Änderung erzwingt eine neue Version;
- Integritätsprüfung erfolgt ausschließlich über SHA‑256 des normativen JSON-Artefakts.

### Freeze Record

`ATLAS_Clarus_Gate-1_Execution_Manifest_v0.1_FROZEN.json`  
`SHA-256 7a887316eac2aa1959459c4a6339502bf324ff3c2213a6e26650fac03bb061bf`

**Freeze state:** `FROZEN / IMMUTABLE / NO-IN-PLACE-EDIT`
