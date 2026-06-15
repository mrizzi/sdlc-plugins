# Version Impact — TC-8005 (CVE-2026-40215)

## Scope

Stream: **2.2.x** (from issue suffix [rhtpa-2.2])
Konflux Release Repo: **rhtpa-release.0.4.z**
Package: **openssl-libs**
Fixed Version: **3.0.7-28.el9_4**
Ecosystem: **RPM** (lock file: rpms.lock.yaml)

## Version Impact Table

| Version | Build | Tag | openssl-libs Version (rpms.lock.yaml) | Affected | Notes |
|---------|-------|-----|---------------------------------------|----------|-------|
| 2.2.0 | 0.4.5 | v0.4.5 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | 0.4.8 | v0.4.8 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | 0.4.9 | v0.4.8 | 3.0.7-27.el9_4 | YES | retag of v0.4.8, carry forward from 2.2.1 |
| 2.2.3 | 0.4.11 | v0.4.11 | 3.0.7-28.el9_4 | NO | >= 3.0.7-28.el9_4 (fixed) |
| 2.2.4 | 0.4.12 | v0.4.12 | 3.0.7-28.el9_4 | NO | >= 3.0.7-28.el9_4 (fixed) |

## Summary

- **Affected versions**: 2.2.0, 2.2.1, 2.2.2
- **Not affected versions**: 2.2.3, 2.2.4
- **Fix first appears in**: 2.2.3 (tag v0.4.11, openssl-libs 3.0.7-28.el9_4)

## Dependency Chain Context

- **Package origin**: explicit install
- **Rationale**: `openssl-libs` IS present in `rpms.lock.yaml` for all tags in the 2.2.x stream, indicating it is an explicitly installed RPM package (not inherited solely from the base image).
- **Lock file**: rpms.lock.yaml
- **Check command**: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`

## Version Comparison Method

RPM version comparison: `3.0.7-25.el9_3 < 3.0.7-27.el9_4 < 3.0.7-28.el9_4`. The release portion (after the hyphen) is compared numerically: 25 < 27 < 28. The `.el9_3` / `.el9_4` dist tags confirm the RHEL 9 target. The fixed version is 3.0.7-28.el9_4, so any version with release < 28 in the 3.0.7 series is affected.
