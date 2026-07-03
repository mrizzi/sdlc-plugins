# Step 2.3.5 -- SBOM Verification Results

## Cosign Availability

```
$ which cosign
/usr/bin/cosign
```

Cosign is available. Proceeding with SBOM verification.

## Classification Comparison: rpms.lock.yaml vs SBOM

For each affected version in the 2.2.x stream (2.2.0, 2.2.1, 2.2.2), the package
origin was classified using both the rpms.lock.yaml (primary) and SBOM comparison
(optional cross-check).

### Version 2.2.0 (tag v0.4.5, openssl-libs 3.0.7-25.el9_3)

| Signal | Present? | Classification |
|--------|----------|----------------|
| rpms.lock.yaml | YES | explicit install |
| Final image SBOM | YES | -- |
| Base image SBOM | YES | base image package |
| **SBOM comparison** | in both final and base | **base image** |

**rpms.lock.yaml classification**: explicit install (package listed in lock file)
**SBOM classification**: base image (present in both final and base image SBOMs)

> WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
> explicit install but SBOM comparison says base image. Investigate manually.

### Version 2.2.1 (tag v0.4.8, openssl-libs 3.0.7-27.el9_4)

| Signal | Present? | Classification |
|--------|----------|----------------|
| rpms.lock.yaml | YES | explicit install |
| Final image SBOM | YES | -- |
| Base image SBOM | YES | base image package |
| **SBOM comparison** | in both final and base | **base image** |

**rpms.lock.yaml classification**: explicit install (package listed in lock file)
**SBOM classification**: base image (present in both final and base image SBOMs)

> WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
> explicit install but SBOM comparison says base image. Investigate manually.

### Version 2.2.2 (retag of 2.2.1, tag v0.4.9, openssl-libs 3.0.7-27.el9_4)

| Signal | Present? | Classification |
|--------|----------|----------------|
| rpms.lock.yaml | YES | explicit install |
| Final image SBOM | YES | -- |
| Base image SBOM | YES | base image package |
| **SBOM comparison** | in both final and base | **base image** |

**rpms.lock.yaml classification**: explicit install (package listed in lock file)
**SBOM classification**: base image (present in both final and base image SBOMs)

> WARNING: SBOM classification disagrees with rpms.lock.yaml -- lock file says
> explicit install but SBOM comparison says base image. Investigate manually.

Note: Version 2.2.2 is a retag of 2.2.1 (backend tag v0.4.9 = v0.4.8). SBOM
verification results are carried forward from 2.2.1 and independently confirmed.

## Summary

| Version | openssl-libs | rpms.lock.yaml | SBOM Comparison | Agreement? |
|---------|-------------|----------------|-----------------|------------|
| 2.2.0 | 3.0.7-25.el9_3 | explicit install | base image | NO |
| 2.2.1 | 3.0.7-27.el9_4 | explicit install | base image | NO |
| 2.2.2 | 3.0.7-27.el9_4 | explicit install | base image | NO |
| 2.2.3 | 3.0.7-28.el9_4 | (not affected -- at fixed version) | -- | -- |
| 2.2.4 | 3.0.7-28.el9_4 | (not affected -- at fixed version) | -- | -- |

All three affected versions show a disagreement between the rpms.lock.yaml
classification (explicit install) and the SBOM comparison classification (base image).
The package appears in the rpms.lock.yaml (suggesting it is explicitly installed),
but the SBOM comparison shows it is present in both the final image and the base
image (suggesting it comes from the base image).

This discrepancy requires manual investigation. Possible explanations:
1. The rpms.lock.yaml may redundantly list a package that is already in the base image
   (explicit reinstall or version override of a base image package)
2. The base image may have been updated to include the package after the rpms.lock.yaml
   was created
3. The package may be installed both explicitly and inherited from the base image
   at different layers

The engineer should investigate to determine the correct remediation path:
- If truly an explicit install: update the package spec in rpms.in.yaml / rpms.lock.yaml
- If truly a base image package: update the base image reference in Dockerfile
