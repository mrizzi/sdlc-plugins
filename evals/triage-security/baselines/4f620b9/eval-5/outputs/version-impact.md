# Step 2 - Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs, versions before 3.0.7-28.el9_4)

Stream scope: **2.2.x** only (per issue suffix `[rhtpa-2.2]`)

| Version | Build | Tag | openssl-libs | Affected? | Notes |
|---------|-------|-----|--------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 3.0.7-25.el9_3 | YES | before fixed version 3.0.7-28.el9_4 |
| 2.2.1 | 0.4.8 | `v0.4.8` | 3.0.7-27.el9_4 | YES | before fixed version 3.0.7-28.el9_4 |
| 2.2.2 | 0.4.9 | `v0.4.9` | — | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 0.4.11 | `v0.4.11` | 3.0.7-28.el9_4 | NO | matches fixed version |
| 2.2.4 | 0.4.12 | `v0.4.12` | 3.0.7-28.el9_4 | NO | matches fixed version |

**Source**: rpms.lock.yaml data extracted via `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'` for each pinned tag in the 2.2.x stream supportability matrix.

## Dependency Chain (Step 2.3.5)

Dependency chain for openssl-libs (RPM):
- rpms.lock.yaml: present (e.g., 3.0.7-27.el9_4 at v0.4.8)
- Origin: **explicit install** (openssl-libs is listed in rpms.lock.yaml)
- Remediation path: update the package version spec in rpms.lock.yaml (or rpms.in.yaml) in the Konflux release repo

Since openssl-libs is an explicit install in rpms.lock.yaml, remediation requires updating the package spec in the Konflux release repo to pin the fixed version (3.0.7-28.el9_4 or later). No base image update is needed.

## Cross-Stream Impact

The 2.1.x stream also ships openssl-libs at potentially vulnerable versions (3.0.7-24.el9 per rpms.lock.yaml), but this issue is scoped to the 2.2.x stream only. Cross-stream impact would be noted as a comment on the Vulnerability issue per Case B, but no remediation tasks are created for the 2.1.x stream from this issue.
