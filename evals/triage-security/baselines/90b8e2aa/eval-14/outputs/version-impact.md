# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs, versions before 3.0.7-28.el9_4)

Stream scope: **2.2.x** (per issue suffix `[rhtpa-2.2]`)

| Version | Build Tag | openssl-libs version | Affected? | Notes |
|---------|-----------|----------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | before fixed version 3.0.7-28.el9_4 |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | before fixed version 3.0.7-28.el9_4 |
| 2.2.2 | v0.4.9 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | ships the fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | ships the fixed version |

## Summary

- **Affected versions**: 2.2.0, 2.2.1, 2.2.2
- **Not affected versions**: 2.2.3, 2.2.4
- Versions 2.2.0 through 2.2.2 ship openssl-libs older than the fixed version 3.0.7-28.el9_4
- Versions 2.2.3 and 2.2.4 already ship the fixed version (3.0.7-28.el9_4)

## Dependency Chain Context (RPM)

openssl-libs is an RPM system package present in the container image.

- **rpms.lock.yaml**: openssl-libs IS present in the lock file for versions 2.2.0 through 2.2.2 --> classified as **explicit install**
- **SBOM comparison**: openssl-libs appears in BOTH the final image SBOM and the base image SBOM --> classified as **base image**
- **Classification disagreement**: rpms.lock.yaml says explicit install, SBOM says base image (see outputs/sbom-verification.md for details)

## Affects Versions Correction (Step 3)

- Current (PSIRT-assigned): `RHTPA 2.0.0`
- Proposed (based on lock file evidence, scoped to 2.2.x stream): `RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2`
- PSIRT version `RHTPA 2.0.0` does not match any version in the 2.2.x supportability matrix -- correction required
