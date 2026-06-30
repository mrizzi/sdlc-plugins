# Step 2.3.5 -- SBOM Verification Results

## Dependency Chain for openssl-libs (RPM)

### Classification Method

Since an RPM lock file (`rpms.lock.yaml`) is configured for the 2.2.x stream, the primary classification source is the lock file. SBOM verification via cosign is used as a secondary cross-check.

- **cosign availability**: YES (`/usr/bin/cosign`)

### Per-Version SBOM Verification

#### Version 2.2.0 (tag v0.4.5)

| Signal | Source | openssl-libs present? | Classification |
|--------|--------|-----------------------|----------------|
| rpms.lock.yaml | `git show v0.4.5:rpms.lock.yaml` | YES (3.0.7-25.el9_3) | explicit install |
| Final image SBOM | `cosign download sbom` | YES | -- |
| Base image SBOM | `cosign download sbom` (base) | YES | base image |

**rpms.lock.yaml classification**: explicit install (package is listed in lock file)
**SBOM classification**: base image (package appears in both final and base image SBOMs)

> :warning: SBOM classification disagrees with rpms.lock.yaml -- lock file says **explicit install** but SBOM comparison says **base image** (present in both final and base image SBOMs). Investigate manually.

#### Version 2.2.1 (tag v0.4.8)

| Signal | Source | openssl-libs present? | Classification |
|--------|--------|-----------------------|----------------|
| rpms.lock.yaml | `git show v0.4.8:rpms.lock.yaml` | YES (3.0.7-27.el9_4) | explicit install |
| Final image SBOM | `cosign download sbom` | YES | -- |
| Base image SBOM | `cosign download sbom` (base) | YES | base image |

**rpms.lock.yaml classification**: explicit install (package is listed in lock file)
**SBOM classification**: base image (package appears in both final and base image SBOMs)

> :warning: SBOM classification disagrees with rpms.lock.yaml -- lock file says **explicit install** but SBOM comparison says **base image** (present in both final and base image SBOMs). Investigate manually.

#### Version 2.2.2 (tag v0.4.9 -- retag of 2.2.1)

| Signal | Source | openssl-libs present? | Classification |
|--------|--------|-----------------------|----------------|
| rpms.lock.yaml | (same as 2.2.1) | YES (3.0.7-27.el9_4) | explicit install |
| Final image SBOM | `cosign download sbom` | YES | -- |
| Base image SBOM | `cosign download sbom` (base) | YES | base image |

**rpms.lock.yaml classification**: explicit install (same as 2.2.1 -- retag)
**SBOM classification**: base image (package appears in both final and base image SBOMs)

> :warning: SBOM classification disagrees with rpms.lock.yaml -- lock file says **explicit install** but SBOM comparison says **base image** (present in both final and base image SBOMs). Investigate manually.

### Versions 2.2.3 and 2.2.4 (not affected)

These versions ship openssl-libs 3.0.7-28.el9_4, which is the fixed version. SBOM verification is not required for non-affected versions.

### Summary Table

| Version | openssl-libs version | rpms.lock.yaml | SBOM (final) | SBOM (base) | rpms.lock.yaml classification | SBOM classification | Agreement? |
|---------|----------------------|----------------|--------------|-------------|-------------------------------|---------------------|------------|
| 2.2.0 | 3.0.7-25.el9_3 | present | present | present | explicit install | base image | NO |
| 2.2.1 | 3.0.7-27.el9_4 | present | present | present | explicit install | base image | NO |
| 2.2.2 | 3.0.7-27.el9_4 | present (retag of 2.2.1) | present | present | explicit install | base image | NO |
| 2.2.3 | 3.0.7-28.el9_4 | -- | -- | -- | -- | -- | N/A (not affected) |
| 2.2.4 | 3.0.7-28.el9_4 | -- | -- | -- | -- | -- | N/A (not affected) |

### Discrepancy Analysis

For all three affected versions (2.2.0, 2.2.1, 2.2.2), the rpms.lock.yaml and SBOM verification signals **disagree**:

- **rpms.lock.yaml** says openssl-libs is an **explicit install** (the package is listed in the lock file, meaning it was explicitly specified as a dependency to install)
- **SBOM comparison** says openssl-libs is a **base image** package (present in both the final image SBOM and the base image SBOM, indicating it is inherited from the base image)

This discrepancy suggests that openssl-libs may be both inherited from the base image AND explicitly pinned/reinstalled in the rpms.lock.yaml. This is a common pattern where a base image package is re-declared in the lock file to pin a specific version. Manual investigation is required to determine:

1. Whether the rpms.lock.yaml entry is intentionally overriding the base image version
2. Whether the remediation path should target the rpms.lock.yaml (explicit pin) or the base image (upstream update), or both
