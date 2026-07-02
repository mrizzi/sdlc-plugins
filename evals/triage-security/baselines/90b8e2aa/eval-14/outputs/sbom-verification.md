# Step 2.3.5 -- SBOM Verification Results

## Package: openssl-libs (RPM)

CVE: CVE-2026-40215
Fixed version: 3.0.7-28.el9_4
cosign availability: YES (/usr/bin/cosign)

## Classification Signals by Version

| Version | Build Tag | openssl-libs version | rpms.lock.yaml | SBOM (final image) | SBOM (base image) | rpms.lock.yaml classification | SBOM classification | Agreement? |
|---------|-----------|----------------------|----------------|---------------------|--------------------|-------------------------------|---------------------|------------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | present | present | present | explicit install | base image | DISAGREE |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | present | present | present | explicit install | base image | DISAGREE |
| 2.2.2 | v0.4.9 | 3.0.7-27.el9_4 | present (retag of v0.4.8) | present | present | explicit install | base image | DISAGREE |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | present | N/A (not affected) | N/A (not affected) | N/A | N/A | N/A |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | present | N/A (not affected) | N/A (not affected) | N/A | N/A | N/A |

## Discrepancy Analysis

For affected versions 2.2.0, 2.2.1, and 2.2.2:

- **rpms.lock.yaml signal**: openssl-libs IS listed in rpms.lock.yaml, which classifies it as an **explicit install** (the package is intentionally specified in the build configuration)
- **SBOM signal**: openssl-libs appears in BOTH the final image SBOM and the base image SBOM, which classifies it as a **base image** package (inherited from the FROM image)

These two signals **disagree**. The rpms.lock.yaml indicates explicit install, but the SBOM comparison indicates base image origin.

### Discrepancy Warning

> SBOM classification disagrees with rpms.lock.yaml -- lock file says explicit install but SBOM comparison says base image. Investigate manually.

This discrepancy could indicate that:
1. The package is both inherited from the base image AND explicitly specified in rpms.lock.yaml (an override or pinning scenario)
2. The rpms.lock.yaml captures all resolved packages including base image packages (not just explicit additions)
3. The package was originally a base image dependency that was later pinned explicitly for version control

**Recommendation**: Investigate the rpms.in.yaml (input specification) to determine whether openssl-libs is intentionally specified as an explicit dependency or if rpms.lock.yaml captures resolved base image packages. This affects the remediation path:
- If truly **explicit install**: update the package spec in rpms.in.yaml/rpms.lock.yaml
- If truly **base image**: update the base image reference in Dockerfile to a version shipping the patched openssl-libs

## SBOM Verification Method

1. cosign confirmed available at `/usr/bin/cosign`
2. Final image SBOM downloaded via: `cosign download sbom <image-reference>@<image-digest>`
3. Base image SBOM downloaded via: `cosign download sbom <base-image-reference>`
4. Both SBOMs searched for `openssl-libs` -- found in both for versions 2.2.0 through 2.2.2
5. Classification: present in both final and base image SBOMs --> base image (per SBOM rules)
6. Cross-checked against rpms.lock.yaml classification --> disagreement flagged
