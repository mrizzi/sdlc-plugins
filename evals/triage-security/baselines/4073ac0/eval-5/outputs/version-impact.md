# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

Scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`.

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 3.0.7-28.el9_4 | NO | ships fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | ships fixed version |

### Source Data

Lock file: `rpms.lock.yaml` in Konflux release repo `rhtpa-release.0.4.z`.

Version data extracted via `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'` at each pinned tag:

- v0.4.5 (2.2.0): openssl-libs 3.0.7-25.el9_3 -- AFFECTED (< 3.0.7-28.el9_4)
- v0.4.8 (2.2.1): openssl-libs 3.0.7-27.el9_4 -- AFFECTED (< 3.0.7-28.el9_4)
- v0.4.9 (2.2.2): retag of v0.4.8 -- same as 2.2.1, AFFECTED
- v0.4.11 (2.2.3): openssl-libs 3.0.7-28.el9_4 -- NOT AFFECTED (= fixed version)
- v0.4.12 (2.2.4): openssl-libs 3.0.7-28.el9_4 -- NOT AFFECTED (= fixed version)

## Dependency Chain (Step 2.3.5)

Dependency chain for openssl-libs (RPM):

- rpms.lock.yaml: openssl-libs IS present -- **explicit install**
- Origin: explicit install (package is specified in rpms.lock.yaml)
- Remediation path: update the package spec in rpms.lock.yaml (or rpms.in.yaml)

## Cross-Stream Observation

The 2.1.x stream (rhtpa-release.0.3.z) is also affected:

- v0.3.8 (2.1.0): openssl-libs 3.0.7-24.el9 -- AFFECTED
- v0.3.12 (2.1.1): openssl-libs 3.0.7-24.el9 -- AFFECTED

However, cross-stream remediation is outside the scope of this issue (scoped to 2.2.x). Cross-stream impact would be noted in a comment on the Vulnerability issue per Case B.
