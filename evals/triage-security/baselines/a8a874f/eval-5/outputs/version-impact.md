# Version Impact Analysis (Step 2)

All versions are analyzed using rpms.lock.yaml data at pinned commits.

## 2.2.x Stream (rhtpa-release.0.4.z)

| Version | Stream | Build Tag | openssl-libs | Affected? | Notes |
|---------|--------|-----------|--------------|-----------|-------|
| 2.2.0 | 2.2.x | v0.4.5 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | 2.2.x | v0.4.8 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | 2.2.x | v0.4.9 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 3.0.7-28.el9_4 | NO | = fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 3.0.7-28.el9_4 | NO | = fixed version |

## Dependency Chain Context

- openssl-libs is a system-level RPM package present in rpms.lock.yaml
- Since it appears in the lock file, this is an **explicit install** (or explicit lock pin), not inherited solely from the base image
- Origin: rpms.lock.yaml (explicit package pin)
