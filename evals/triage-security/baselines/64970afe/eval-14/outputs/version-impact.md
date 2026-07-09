# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

Source: `security-matrix.md` for `rhtpa-release.0.4.z`

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

Matrix Last-Updated: 2026-06-28T10:00:00Z (11 days ago -- within 14-day freshness threshold)

## 2.3 -- Dependency Version Extraction

Ecosystem: RPM
Lock file: `rpms.lock.yaml`
Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
Fix threshold: 3.0.7-28.el9_4

| Version | Tag | openssl-libs version | Affected? | Notes |
|---------|-----|----------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | = fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | = fixed version |

## 2.3.5 -- Dependency Chain Context

### Version 2.2.0 (v0.4.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-25.el9_3) -> explicit install
  SBOM verification (cosign available at /usr/bin/cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM classification: base image (present in both final and base image SBOMs)
    rpms.lock.yaml classification: explicit install (present in lock file)
    WARNING: SBOM classification DISAGREES with rpms.lock.yaml -- lock file says
    explicit install but SBOM comparison says base image. Investigate manually.
  Origin: DISPUTED -- rpms.lock.yaml indicates explicit install, SBOM indicates base image

Remediation: investigate the discrepancy between rpms.lock.yaml (explicit install)
and SBOM analysis (base image origin) before determining the remediation path.
If explicit install: update the package spec in rpms.in.yaml / rpms.lock.yaml.
If base image: update base image tag to a version with patched openssl-libs.
```

### Version 2.2.1 (v0.4.8)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-27.el9_4) -> explicit install
  SBOM verification (cosign available at /usr/bin/cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM classification: base image (present in both final and base image SBOMs)
    rpms.lock.yaml classification: explicit install (present in lock file)
    WARNING: SBOM classification DISAGREES with rpms.lock.yaml -- lock file says
    explicit install but SBOM comparison says base image. Investigate manually.
  Origin: DISPUTED -- rpms.lock.yaml indicates explicit install, SBOM indicates base image

Remediation: investigate the discrepancy between rpms.lock.yaml (explicit install)
and SBOM analysis (base image origin) before determining the remediation path.
If explicit install: update the package spec in rpms.in.yaml / rpms.lock.yaml.
If base image: update base image tag to a version with patched openssl-libs.
```

### Version 2.2.2 (v0.4.9) -- retag of 2.2.1

```
Dependency chain for openssl-libs (RPM):
  Retag of 2.2.1 (v0.4.8) -- same source commits, same dependency chain.
  rpms.lock.yaml: present (3.0.7-27.el9_4) -> explicit install
  SBOM verification (cosign available at /usr/bin/cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM classification: base image (present in both final and base image SBOMs)
    rpms.lock.yaml classification: explicit install (present in lock file)
    WARNING: SBOM classification DISAGREES with rpms.lock.yaml -- lock file says
    explicit install but SBOM comparison says base image. Investigate manually.
  Origin: DISPUTED -- same as 2.2.1

Remediation: same as 2.2.1.
```

### Versions 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12)

```
Not affected -- openssl-libs at 3.0.7-28.el9_4 (= fixed version).
No dependency chain analysis required.
```

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs, versions before 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | explicit install per rpms.lock.yaml; SBOM disagrees (base image) |
| 2.2.1 | 3.0.7-27.el9_4 | YES | explicit install per rpms.lock.yaml; SBOM disagrees (base image) |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 3.0.7-28.el9_4 | NO | = fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | = fixed version |

### Summary

- **Affected versions**: 2.2.0, 2.2.1, 2.2.2
- **Not affected versions**: 2.2.3, 2.2.4
- **Fix threshold**: 3.0.7-28.el9_4
- **First fixed version in stream**: 2.2.3 (build 0.4.11, 2026-03-23)
- **SBOM discrepancy**: For all affected versions (2.2.0--2.2.2), rpms.lock.yaml classifies openssl-libs as an explicit install, but SBOM comparison (final image vs base image) classifies it as a base image package. This discrepancy requires manual investigation before determining the remediation path.

### Cross-Stream Impact

The issue is scoped to the 2.2.x stream via the `[rhtpa-2.2]` suffix. The 2.1.x stream also ships openssl-libs at vulnerable versions (3.0.7-24.el9 for both 2.1.0 and 2.1.1), but cross-stream remediation is tracked separately per the scoped issue protocol.

| Stream | Versions affected | openssl-libs versions |
|--------|-------------------|-----------------------|
| 2.1.x | 2.1.0, 2.1.1 | 3.0.7-24.el9 (both) |
| 2.2.x (in scope) | 2.2.0, 2.2.1, 2.2.2 | 3.0.7-25.el9_3, 3.0.7-27.el9_4 |
