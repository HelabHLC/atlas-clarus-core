# GitHub Setup Recommendation

## Recommended repository

**Name**

```text
atlas-clarus
```

**Description**

```text
Documented colour-reference identity for open creative tools. Deterministic ATLAS binding before production translation; Public Beta integrations for Inkscape, GIMP and Krita.
```

**Suggested topics**

```text
colour
color
colour-science
color-management
gimp
krita
inkscape
hlc
reproducibility
prepress
open-tools
```

## Why a separate repository

The existing `arbe-lambda` repository defines a spectral metric/toolchain. ATLAS Clarus has a different primary responsibility: documented reference identity and its separation from production feasibility, device values and measured QC.

Keeping separate repositories avoids conflating:

- spectral metrics;
- colour-reference identity;
- application integrations;
- physical measurement claims.

Cross-link the projects where they genuinely interact.

## First commit

Suggested commit message:

```text
feat: publish ATLAS Clarus open-tool integration milestone
```

## Optional follow-up commits

```text
docs: add per-application validation manifests
test: add reproducible colour-binding fixtures
docs: publish integration installation instructions
chore: add release checksums and provenance inventory
```
