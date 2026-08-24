# Installation — ATLAS Clarus × GIMP v0.1.3

## Requirements

- GIMP 3.2.x with Python 3 / GI plug-in support
- an RGB image using U8 non-linear precision and an effective sRGB profile for the normative document-pixel route

## Install

1. Close GIMP.
2. Extract `atlas-clarus-pkl-gimp.zip`.
3. Copy the entire folder `atlas-clarus-pkl-gimp` into the GIMP user plug-ins directory.
4. On the validated Windows installation the path was `%APPDATA%\GIMP\3.2\plug-ins\`.
5. Restart GIMP.
6. Open an image and confirm `Colors → ATLAS Clarus` contains both procedures.

On Unix-like systems, make `atlas-clarus-pkl-gimp.py` executable if required.

## Procedures

- `Match Document Pixel by XY…` — normative gated document-pixel route
- `Match Current Foreground` — convenience route for explicit sRGB input; it does not prove document-pixel provenance

Save original images separately. Setting the matched PKL as foreground is optional and occurs only after source identity has been frozen.
