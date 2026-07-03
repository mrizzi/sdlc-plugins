# Step 2.3.5 -- SBOM Verification Results

## Dependency Chain for openssl-libs (RPM)

Ecosystem: RPM (system package)
cosign availability: YES (`/usr/bin/cosign`)

## Classification Signals by Version

### Version 2.2.0 (tag v0.4.5)

| Signal | Result | Classification |
|--------|--------|----------------|
| rpms.lock.yaml | openssl-libs **present** (3.0.7-25.el9_3) | explicit install |
| SBOM (final image) | openssl-libs **present** | -- |
| SBOM (base image) | openssl-libs **present** | base image |
| SBOM comparison | present in **both** final and base image SBOMs | base image origin |

> **SBOM classification disagrees with rpms.lock.yaml** -- lock file says **explicit install** but SBOM comparison says **base image**. Investigate manually.

### Version 2.2.1 (tag v0.4.8)

| Signal | Result | Classification |
|--------|--------|----------------|
| rpms.lock.yaml | openssl-libs **present** (3.0.7-27.el9_4) | explicit install |
| SBOM (final image) | openssl-libs **present** | -- |
| SBOM (base image) | openssl-libs **present** | base image |
| SBOM comparison | present in **both** final and base image SBOMs | base image origin |

> **SBOM classification disagrees with rpms.lock.yaml** -- lock file says **explicit install** but SBOM comparison says **base image**. Investigate manually.

### Version 2.2.2 (tag v0.4.9 -- retag of v0.4.8)

| Signal | Result | Classification |
|--------|--------|----------------|
| rpms.lock.yaml | openssl-libs **present** (3.0.7-27.el9_4) | explicit install |
| SBOM (final image) | openssl-libs **present** | -- |
| SBOM (base image) | openssl-libs **present** | base image |
| SBOM comparison | present in **both** final and base image SBOMs | base image origin |

> **SBOM classification disagrees with rpms.lock.yaml** -- lock file says **explicit install** but SBOM comparison says **base image**. Investigate manually.

Same as version 2.2.1 (retag -- identical source commits).

### Version 2.2.3 (tag v0.4.11) -- NOT AFFECTED

openssl-libs version 3.0.7-28.el9_4 equals the fixed version. SBOM verification not required for non-affected versions.

### Version 2.2.4 (tag v0.4.12) -- NOT AFFECTED

openssl-libs version 3.0.7-28.el9_4 equals the fixed version. SBOM verification not required for non-affected versions.

## Summary

For all affected versions (2.2.0, 2.2.1, 2.2.2), the two classification signals **disagree**:

| Version | rpms.lock.yaml | SBOM Comparison | Agreement? |
|---------|----------------|-----------------|------------|
| 2.2.0 | explicit install (present in lock file) | base image (present in both SBOMs) | NO |
| 2.2.1 | explicit install (present in lock file) | base image (present in both SBOMs) | NO |
| 2.2.2 | explicit install (present in lock file) | base image (present in both SBOMs) | NO |

This discrepancy means the package appears in rpms.lock.yaml (indicating it was explicitly installed) but the SBOM comparison shows it is also present in the base image. This could indicate that:

1. The package is explicitly pinned in rpms.lock.yaml to control the version, even though the base image already provides it.
2. The rpms.lock.yaml may be re-declaring a base image package for version pinning purposes.

**Recommendation**: Manual investigation is required to determine the correct remediation path. If the package is truly a base image dependency that is re-declared in rpms.lock.yaml for version control, remediation may require both a base image update and an rpms.lock.yaml update.
