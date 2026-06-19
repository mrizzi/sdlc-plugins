# Step 2 -- Version Impact Analysis

## 2.2.x Stream (scoped by issue suffix `[rhtpa-2.2]`)

### Supportability Matrix

Source: security-matrix.md for rhtpa-release.0.4.z (2.2.x stream)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

### Dependency Version Extraction (rpms.lock.yaml)

Lock file inspection commands (simulated from mock data):

```
git show v0.4.5:rpms.lock.yaml | grep 'openssl-libs'   -> 3.0.7-25.el9_3
git show v0.4.8:rpms.lock.yaml | grep 'openssl-libs'   -> 3.0.7-27.el9_4
git show v0.4.9:rpms.lock.yaml | grep 'openssl-libs'   -> (retag of v0.4.8)
git show v0.4.11:rpms.lock.yaml | grep 'openssl-libs'  -> 3.0.7-28.el9_4
git show v0.4.12:rpms.lock.yaml | grep 'openssl-libs'  -> 3.0.7-28.el9_4
```

### Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs versions before 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|--------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 3.0.7-28.el9_4 | NO | = fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | = fixed version |

**Summary**: 3 of 5 versions in the 2.2.x stream are affected (2.2.0, 2.2.1, 2.2.2).
Versions 2.2.3 and 2.2.4 ship the fixed version (3.0.7-28.el9_4) and are NOT affected.

### Dependency Chain Context (Step 2.3.5)

Ecosystem: RPM (container-level dependency)

**Package origin classification:**

openssl-libs is present in `rpms.lock.yaml` at all checked tags (v0.4.5, v0.4.8, v0.4.11, v0.4.12). Per the classification rules:

- **In lock file** --> **explicit install**

The package is explicitly installed via the RPM lock file, not inherited from the base image. Remediation path: update the package spec in `rpms.lock.yaml` (or the corresponding `rpms.in.yaml` input file) and regenerate the lock file.

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: PRESENT -> explicit install
  Origin: explicit install (openssl-libs is specified in rpms.lock.yaml)

Remediation: update openssl-libs to >= 3.0.7-28.el9_4 in rpms.lock.yaml
(or rpms.in.yaml input file) and regenerate.
```
