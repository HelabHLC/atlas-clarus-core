# Third-Party Data and Notices

ATLAS Clarus relies on external colour-reference resources whose licences and provenance must be preserved.

## HLC Colour Atlas XL

Original HLC Colour Atlas XL data: Copyright (c) freieFarbe e.V.

The 2019 v1.2 package readme identifies the package as CC BY-ND 4.0. The
publisher's current, product-specific licence page separately states that
database products — explicitly including HLC Colour Atlas CxF and ASE files —
are released under the zlib licence, which permits alteration and
redistribution when origin and modification are identified and the notice is
preserved.

ATLAS Clarus relies on that current zlib permission for machine-readable
derived data. Derived files are plainly marked and are not represented as
unmodified freieFarbe source files.

- Publisher: https://freiefarbe.de/
- Current licence page: https://freiefarbe.de/licence/
- Official download page: https://freiefarbe.de/en/thema-farbe/software/
- Official v1.2 package SHA-256:
  `49d0bc10aeb90ee4b6f30d20305dd919caa37eca94e81a80ebf8e23b36ed1bdd`

See [`docs/LICENSE_AUDIT_HLC_ATLAS_XL.md`](docs/LICENSE_AUDIT_HLC_ATLAS_XL.md).

Required notice for derived data:

```text
Original HLC Colour Atlas XL data:
Copyright (c) freieFarbe e.V.
Modified/derived by the ATLAS Clarus project.
```

## ICC and FOGRA material

ICC profiles and FOGRA reference material may have their own distribution terms.

Do not add them to a public repository until redistribution rights have been checked.

## ATLAS Clarus software licence

ATLAS Clarus software code in this repository is published under the MIT License; see [`LICENSE`](LICENSE).

This licence does not relicense third-party reference data, ICC profiles, FOGRA material or other upstream assets. Application-specific data notices remain authoritative for bundled reference material.
