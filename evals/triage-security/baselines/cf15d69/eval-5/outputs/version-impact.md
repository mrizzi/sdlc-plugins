# Step 2 -- Version Impact Analysis

## Scoped Stream: 2.2.x (rhtpa-release.0.4.z)

The issue is scoped to the 2.2.x stream per the `[rhtpa-2.2]` suffix. Version impact analysis covers all versions in the 2.2.x supportability matrix.

## Fix Threshold

- Vulnerable package: openssl-libs
- Affected range: versions before 3.0.7-28.el9_4
- Fixed version: 3.0.7-28.el9_4

## Lock File Data (rpms.lock.yaml)

Extracted via `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'` for each pinned tag in the 2.2.x supportability matrix:

| Tag | openssl-libs version |
|-----|----------------------|
| v0.4.5 | 3.0.7-25.el9_3 |
| v0.4.8 | 3.0.7-27.el9_4 |
| v0.4.9 | (retag of v0.4.8) |
| v0.4.11 | 3.0.7-28.el9_4 |
| v0.4.12 | 3.0.7-28.el9_4 |

## Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | Build | openssl-libs | Affected? | Notes |
|---------|-------|--------------|-----------|-------|
| 2.2.0 | 0.4.5 | 3.0.7-25.el9_3 | YES | below fix threshold |
| 2.2.1 | 0.4.8 | 3.0.7-27.el9_4 | YES | below fix threshold |
| 2.2.2 | 0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.11 | 3.0.7-28.el9_4 | NO | at fix threshold |
| 2.2.4 | 0.4.12 | 3.0.7-28.el9_4 | NO | at fix threshold |

## Dependency Chain Context (Step 2.3.5)

Dependency chain for openssl-libs (RPM):
- rpms.lock.yaml: PRESENT -- explicit install (package is listed in rpms.lock.yaml)
- Origin: explicit install via rpms.lock.yaml
- Remediation: update openssl-libs version spec in rpms.lock.yaml (or rpms.in.yaml) to >= 3.0.7-28.el9_4

## Cross-Stream Impact (informational)

Although this issue is scoped to the 2.2.x stream, the mock data also shows the 2.1.x stream ships vulnerable openssl-libs versions:

| Version | openssl-libs | Affected? |
|---------|--------------|-----------|
| 2.1.0 | 3.0.7-24.el9 | YES |
| 2.1.1 | 3.0.7-24.el9 | YES |

This cross-stream impact would be reported in Step 7 Case B.

## Summary

- Affected versions in 2.2.x stream: **2.2.0, 2.2.1, 2.2.2**
- Not affected versions in 2.2.x stream: **2.2.3, 2.2.4**
- The fix was introduced in build 0.4.11 (version 2.2.3) which ships openssl-libs 3.0.7-28.el9_4
