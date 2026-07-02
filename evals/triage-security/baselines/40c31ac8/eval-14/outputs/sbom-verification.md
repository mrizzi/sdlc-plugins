# Step 2.3.5 -- SBOM Verification Results: CVE-2026-40215

## Cosign Availability

```
$ which cosign
/usr/bin/cosign
```

cosign is available. SBOM verification will be performed.

## SBOM Verification for Affected Versions (2.2.x stream)

For each affected version, the rpms.lock.yaml classification is compared against
the SBOM-based classification (final image SBOM vs. base image SBOM).

### Version 2.2.0 (tag v0.4.5)

| Signal | Result | Classification |
|--------|--------|----------------|
| rpms.lock.yaml | openssl-libs **present** | Explicit install |
| Final image SBOM | openssl-libs **present** (3.0.7-25.el9_3) | -- |
| Base image SBOM | openssl-libs **present** | Base image origin |
| SBOM comparison | In BOTH final and base image SBOMs | Base image origin |

**DISAGREEMENT DETECTED**

rpms.lock.yaml says: **explicit install** (package is listed in the lock file)
SBOM comparison says: **base image** (package appears in both final and base image SBOMs)

### Version 2.2.1 (tag v0.4.8)

| Signal | Result | Classification |
|--------|--------|----------------|
| rpms.lock.yaml | openssl-libs **present** | Explicit install |
| Final image SBOM | openssl-libs **present** (3.0.7-27.el9_4) | -- |
| Base image SBOM | openssl-libs **present** | Base image origin |
| SBOM comparison | In BOTH final and base image SBOMs | Base image origin |

**DISAGREEMENT DETECTED**

rpms.lock.yaml says: **explicit install** (package is listed in the lock file)
SBOM comparison says: **base image** (package appears in both final and base image SBOMs)

### Version 2.2.2 (tag v0.4.9 -- retag of v0.4.8)

| Signal | Result | Classification |
|--------|--------|----------------|
| rpms.lock.yaml | openssl-libs **present** (same as 2.2.1) | Explicit install |
| Final image SBOM | openssl-libs **present** (3.0.7-27.el9_4, same as 2.2.1) | -- |
| Base image SBOM | openssl-libs **present** | Base image origin |
| SBOM comparison | In BOTH final and base image SBOMs | Base image origin |

**DISAGREEMENT DETECTED**

rpms.lock.yaml says: **explicit install** (package is listed in the lock file)
SBOM comparison says: **base image** (package appears in both final and base image SBOMs)

## Summary of Disagreements

| Version | rpms.lock.yaml | SBOM Comparison | Agreement? |
|---------|----------------|-----------------|------------|
| 2.2.0 | Explicit install | Base image | **NO** |
| 2.2.1 | Explicit install | Base image | **NO** |
| 2.2.2 | Explicit install | Base image | **NO** |

All three affected versions show the same disagreement pattern.

## Engineer Action Required

The rpms.lock.yaml classification and SBOM verification disagree for all affected versions (2.2.0, 2.2.1, 2.2.2):

- **rpms.lock.yaml** lists openssl-libs as an explicit package, classifying it as an **explicit install**. This would mean remediation is: update the package spec in rpms.in.yaml / rpms.lock.yaml.

- **SBOM comparison** shows openssl-libs in **both** the final image SBOM and the base image SBOM, classifying it as a **base image** package. This would mean remediation is: update the base image tag/digest to a version that includes patched openssl-libs.

This disagreement likely means the package is inherited from the base image **and** also explicitly listed in rpms.lock.yaml (possibly as a version pin or override). The engineer should investigate:

1. Check `rpms.in.yaml` to determine if openssl-libs is intentionally pinned or if the lock file entry is a transitive inclusion
2. Check the Dockerfile `FROM` line to identify the base image and whether it already provides openssl-libs
3. Determine the correct remediation path:
   - If the lock file pin is intentional: update the pin in rpms.in.yaml and regenerate rpms.lock.yaml
   - If the lock file entry is inherited/automatic: update the base image reference to pick up the fix

Until this disagreement is resolved, the remediation task template should note both possible paths.
