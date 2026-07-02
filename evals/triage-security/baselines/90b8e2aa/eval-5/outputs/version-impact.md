# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

### Scoped stream: 2.2.x (rhtpa-release.0.4.z)

| Version | Build Tag | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|-----------|-------------------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | = fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | = fixed version |

### Cross-stream analysis: 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|-----------|-------------------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |

## Dependency Chain (Step 2.3.5)

### Package classification

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install
  SBOM verification: skipped -- cosign not available
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation: update the package spec in rpms.lock.yaml.
```

- **Origin**: explicit install -- openssl-libs is present in `rpms.lock.yaml`
  at the pinned build tags for all 2.2.x versions, confirming it is an explicitly
  managed package (not inherited from the base image).
- **SBOM verification**: cosign is not available in this environment. SBOM
  comparison between final container image and base image was skipped. Using
  rpms.lock.yaml classification only.
- **Remediation path**: Since openssl-libs is an explicit install in
  rpms.lock.yaml, remediation involves updating the package version spec in the
  lock file (or rpms.in.yaml). No base image update is needed.
- **Introduction point**: openssl-libs is present across all versions in both
  the 2.1.x and 2.2.x streams. It is a long-standing explicit dependency.

## Summary

- **2.2.x stream**: Versions 2.2.0, 2.2.1, and 2.2.2 ship vulnerable openssl-libs.
  Versions 2.2.3 and 2.2.4 already ship the fixed version (3.0.7-28.el9_4).
  The fix was picked up in build 0.4.11 (2.2.3, released 2026-03-23).
- **2.1.x stream (cross-stream)**: All versions (2.1.0, 2.1.1) ship vulnerable
  openssl-libs (3.0.7-24.el9). No version in the 2.1.x stream has the fix.
