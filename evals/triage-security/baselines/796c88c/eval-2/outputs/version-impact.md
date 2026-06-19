# Version Impact Analysis: TC-8002 (CVE-2026-28940)

## Vulnerability Criteria

- **Library**: serde_json
- **Affected range**: < 1.0.135
- **Fixed version**: 1.0.135

A version is affected only if its pinned serde_json version is **less than 1.0.135**.

## Stream: 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Backend Tag | serde_json Version | Affected? |
|---------|-------|-------------|-------------------|-----------|
| 2.1.0 | 0.3.8 | `v0.3.8` | 1.0.137 | No (>= 1.0.135) |
| 2.1.1 | 0.3.12 | `v0.3.12` | 1.0.137 | No (>= 1.0.135) |

## Stream: 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Backend Tag | serde_json Version | Affected? | Notes |
|---------|-------|-------------|-------------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 1.0.138 | No (>= 1.0.135) | |
| 2.2.1 | 0.4.8 | `v0.4.8` | 1.0.138 | No (>= 1.0.135) | |
| 2.2.2 | 0.4.9 | `v0.4.8` | 1.0.138 | No (>= 1.0.135) | Retag of 2.2.1; carried forward from v0.4.8 |
| 2.2.3 | 0.4.11 | `v0.4.11` | 1.0.139 | No (>= 1.0.135) | |
| 2.2.4 | 0.4.12 | `v0.4.12` | 1.0.139 | No (>= 1.0.135) | |

## Retag Handling

- **Version 2.2.2** (build 0.4.9): The supportability matrix notes "backend retag of 2.2.1". The backend tag is `v0.4.8` (same as 2.2.1). The lock file check is skipped for this version; the serde_json version is carried forward from `v0.4.8` = **1.0.138**.

## Summary

**0 of 7 supported versions are affected.**

All supported versions across both streams (2.1.x and 2.2.x) ship serde_json >= 1.0.137, which is above the fix threshold of 1.0.135. The vulnerability is not present in any supported release.
