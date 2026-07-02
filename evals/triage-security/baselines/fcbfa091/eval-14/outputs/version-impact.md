# Step 2 — Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

Stream scope: **2.2.x** only (from issue suffix [rhtpa-2.2])

| Version | Tag | openssl-libs version | Affected? | Notes |
|---------|-----|----------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | v0.4.9 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | = fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | = fixed version |

## Summary

Versions 2.2.0, 2.2.1, and 2.2.2 ship a vulnerable version of openssl-libs (before 3.0.7-28.el9_4). Versions 2.2.3 and 2.2.4 ship the fixed version (3.0.7-28.el9_4) and are not affected.

## Dependency Chain Context

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (versions 2.2.0–2.2.2) → explicit install
  SBOM verification (cosign): present in BOTH final image SBOM and base image SBOM → base image

  ⚠️ SBOM classification disagrees with rpms.lock.yaml — lock file says explicit install
  but SBOM comparison says base image. Investigate manually.

  rpms.lock.yaml remains the primary signal. The package is classified as explicit install
  based on lock file presence, but the SBOM cross-check indicates the package may also be
  inherited from the base image. This discrepancy should be investigated to determine
  the correct remediation path.

  Remediation (per rpms.lock.yaml classification — explicit install):
  Update the package spec in rpms.in.yaml / rpms.lock.yaml to >= 3.0.7-28.el9_4.
```
