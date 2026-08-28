# Licence Audit — freieFarbe HLC Colour Atlas XL

Audit date: 2026-08-28

Status: `REDISTRIBUTION PERMITTED WITH ATTRIBUTION AND MODIFICATION NOTICE`

This is a project licence assessment, not legal advice.

## Source package verified

Official package:

`HLC-Colour-Atlas-XL_Set_DE_v1-2.zip`

SHA-256:

`49d0bc10aeb90ee4b6f30d20305dd919caa37eca94e81a80ebf8e23b36ed1bdd`

Publisher: freieFarbe e.V.

Official download page:

https://freiefarbe.de/en/thema-farbe/software/

## Licence history and current grant

The readme bundled with the 2019 v1.2 package states CC BY-ND 4.0 and permits
private and commercial copying of the data in unchanged form with attribution.

The publisher's current licence page makes a more specific distinction:

- atlas PDF files are given as an example of CC BY-ND 4.0 material;
- database products, explicitly including freieFarbe HLC Colour Atlas CxF and
  ASE files, are published under the zlib licence;
- the zlib grant permits commercial use, alteration and redistribution;
- altered source versions must be clearly marked and must not be represented
  as the original data;
- the origin and notice must be preserved.

Current licence page:

https://freiefarbe.de/licence/

The repository relies on this current, product-specific zlib permission for
the modified and derived machine-readable data. The older bundled CC BY-ND
notice is retained in this audit to make the licence history transparent.

## Required attribution

```text
Original HLC Colour Atlas XL data:
Copyright (c) freieFarbe e.V.
https://freiefarbe.de/

Original data product: HLC Colour Atlas XL v1.2
Official package SHA-256:
49d0bc10aeb90ee4b6f30d20305dd919caa37eca94e81a80ebf8e23b36ed1bdd

Modified/derived by the ATLAS Clarus project.
These derived files are not the unmodified freieFarbe source files.
```

## Repository treatment

- The original CxF and official ZIP are not committed.
- Their filenames and SHA-256 values are recorded as external inputs.
- Derived Shadow Master and digest mappings are plainly labelled modified.
- ATLAS Clarus software remains MIT-licensed.
- The MIT licence does not replace the upstream data notice.

