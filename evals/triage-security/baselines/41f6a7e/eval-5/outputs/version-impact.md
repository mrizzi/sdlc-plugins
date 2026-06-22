# Step 2 -- Version Impact Analysis

## Supportability Matrix (2.2.x stream)

Source: `security-matrix.md` for `rhtpa-release.0.4.z`

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | |

## Lock File Evidence (rpms.lock.yaml)

Dependency versions extracted via `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`:

| Tag | openssl-libs version |
|-----|----------------------|
| v0.4.5 | 3.0.7-25.el9_3 |
| v0.4.8 | 3.0.7-27.el9_4 |
| v0.4.9 | _(retag of v0.4.8)_ |
| v0.4.11 | 3.0.7-28.el9_4 |
| v0.4.12 | 3.0.7-28.el9_4 |

## Version Impact Table

CVE-2026-40215 (openssl-libs, affected: versions before 3.0.7-28.el9_4, fixed: 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | before fixed version 3.0.7-28.el9_4 |
| 2.2.1 | 3.0.7-27.el9_4 | YES | before fixed version 3.0.7-28.el9_4 |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 3.0.7-28.el9_4 | NO | ships fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | ships fixed version |

## Dependency Chain Context (Step 2.3.5)

Dependency chain for openssl-libs (RPM):

- rpms.lock.yaml: openssl-libs IS present in lock file -- explicit install
- Origin: **explicit install** (package is specified in rpms.lock.yaml / rpms.in.yaml)
- Remediation path: update the package spec in rpms.lock.yaml (or rpms.in.yaml) in the Konflux release repo

The package is present in rpms.lock.yaml for all 2.2.x versions, confirming it is an explicitly managed RPM dependency (not inherited from the base image). The fix requires updating the openssl-libs package spec to >= 3.0.7-28.el9_4 in the Konflux release repo.

## Cross-Stream Impact

The 2.1.x stream is also affected based on lock file data:

| Version | openssl-libs | Affected? |
|---------|-------------|-----------|
| 2.1.0 | 3.0.7-24.el9 | YES |
| 2.1.1 | 3.0.7-24.el9 | YES |

However, since this issue is scoped to the 2.2.x stream per suffix `[rhtpa-2.2]`, the 2.1.x impact is informational only. A companion PSIRT issue should track the 2.1.x stream separately.
