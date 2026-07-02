# Step 2.3.5 — SBOM Verification Results

## Package: openssl-libs (RPM)

cosign is available at `/usr/bin/cosign`.

## Verification Results by Version

| Version | Tag | rpms.lock.yaml | rpms.lock.yaml Classification | SBOM (final image) | SBOM (base image) | SBOM Classification | Agreement? |
|---------|-----|----------------|-------------------------------|--------------------|--------------------|---------------------|------------|
| 2.2.0 | v0.4.5 | present | explicit install | present | present | base image | DISAGREE |
| 2.2.1 | v0.4.8 | present | explicit install | present | present | base image | DISAGREE |
| 2.2.2 | v0.4.9 | present (retag of v0.4.8) | explicit install | present | present | base image | DISAGREE |
| 2.2.3 | v0.4.11 | present | not affected (fixed version) | — | — | — | N/A (not affected) |
| 2.2.4 | v0.4.12 | present | not affected (fixed version) | — | — | — | N/A (not affected) |

## Classification Details

**rpms.lock.yaml signal**: openssl-libs is listed in `rpms.lock.yaml` for all tags (v0.4.5, v0.4.8, v0.4.9, v0.4.11, v0.4.12). Per the classification rules, presence in the lock file means **explicit install**.

**SBOM signal (cosign download sbom)**: For affected versions 2.2.0 through 2.2.2, `cosign download sbom` was used to compare the final container image SBOM against the base image SBOM. openssl-libs appears in **both** the final image SBOM and the base image SBOM, which indicates a **base image** origin.

## Discrepancy Warning

> ⚠️ SBOM classification disagrees with rpms.lock.yaml for versions 2.2.0, 2.2.1, and 2.2.2.
>
> - **rpms.lock.yaml says**: explicit install (package is listed in the lock file)
> - **SBOM comparison says**: base image (package present in both final and base image SBOMs)
>
> **rpms.lock.yaml remains the primary signal.** The lock file is the source of truth for classification per the ecosystem mappings configuration. However, the SBOM cross-check suggests the package may also be inherited from the base image.
>
> This could indicate that openssl-libs is both explicitly installed in `rpms.in.yaml` AND present in the base image. The explicit install may be pinning or overriding a base image package. Investigate manually to determine:
> 1. Whether the explicit install in rpms.lock.yaml is intentional (e.g., to pin a specific version)
> 2. Whether removing the explicit install would cause the base image version to be used instead
> 3. The correct remediation path — update rpms.in.yaml/rpms.lock.yaml (explicit install path) or update the base image tag (base image path), or both

## SBOM Verification Not Performed for Unaffected Versions

Versions 2.2.3 and 2.2.4 ship openssl-libs 3.0.7-28.el9_4, which is the fixed version. SBOM verification was not performed for these versions as they are not affected by CVE-2026-40215.
