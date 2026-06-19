# Step 2 — Version Impact Analysis

## CVE-2026-40215 — openssl-libs (versions before 3.0.7-28.el9_4)

The issue is scoped to the **2.2.x** stream. The supportability matrix for the
2.2.x stream is in `rhtpa-release.0.4.z`. All versions in this stream are analyzed
using `rpms.lock.yaml` data at pinned commits.

### Version Impact Table

| Version | Build Tag | openssl-libs version | Affected? | Notes |
|---------|-----------|----------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | v0.4.9 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | = fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | = fixed version |

### Cross-stream Analysis (informational)

The issue is scoped to 2.2.x only. For informational purposes, the 2.1.x stream
(rhtpa-release.0.3.z) is also affected:

| Version | Build Tag | openssl-libs version | Affected? | Notes |
|---------|-----------|----------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |

### Dependency Chain Context (RPM)

openssl-libs is a system-level RPM package present in rpms.lock.yaml. Since it
appears in the lock file, this is an **explicit install** (or explicit lock pin),
not inherited solely from the base image.

- **Origin**: rpms.lock.yaml (explicit package pin)
- **Remediation path**: Update the openssl-libs entry in rpms.lock.yaml
  (or rpms.in.yaml) to >= 3.0.7-28.el9_4, then regenerate the lock file.
- **Advisory**: RHSA-2026:4021 provides the patched RPM.

### Summary

- Versions 2.2.0, 2.2.1, and 2.2.2 are **affected** (ship openssl-libs < 3.0.7-28.el9_4).
- Versions 2.2.3 and 2.2.4 are **not affected** (ship openssl-libs 3.0.7-28.el9_4, the fixed version).
- The fix was picked up in build v0.4.11 (version 2.2.3).
