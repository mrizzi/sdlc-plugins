# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

Source: security-matrix.md for rhtpa-release.0.4.z

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | |

## 2.3 -- Dependency Version Extraction (rpms.lock.yaml)

Ecosystem: RPM
Lock file: rpms.lock.yaml
Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`

Extracted openssl-libs versions for the 2.2.x stream:

| Version | Tag | openssl-libs version | Source |
|---------|-----|----------------------|--------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | rpms.lock.yaml |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | rpms.lock.yaml |
| 2.2.2 | v0.4.9 | _(retag of v0.4.8)_ | same as 2.2.1 |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | rpms.lock.yaml |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | rpms.lock.yaml |

## 2.3.5 -- Dependency Chain Context

Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: PRESENT (openssl-libs found in lock file)
  Origin: explicit install (package is specified in rpms.lock.yaml)

  Remediation path: update the openssl-libs package spec in rpms.lock.yaml
  (or rpms.in.yaml) to >= 3.0.7-28.el9_4, then regenerate the lock file.

  Advisory: RHSA-2026:4021 provides the patched RPM (3.0.7-28.el9_4).

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

**Scoped stream: 2.2.x**

| Version | openssl-libs | Affected? | Notes |
|---------|--------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 3.0.7-28.el9_4 | NO | = fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | = fixed version |

**Cross-stream check: 2.1.x** (out of scope but checked for Case B)

| Version | openssl-libs | Affected? | Notes |
|---------|--------------|-----------|-------|
| 2.1.0 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |
| 2.1.1 | 3.0.7-24.el9 | YES | < 3.0.7-28.el9_4 |

## 2.5 -- Upstream Fix Check

Not applicable for RPM ecosystem. RPM packages do not have an upstream branch in the source repository. The fix is delivered via the Red Hat errata (RHSA-2026:4021) and consumed by updating rpms.lock.yaml in the Konflux release repo.

## Summary

- **2.2.x stream (scoped)**: versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fixed openssl-libs (3.0.7-28.el9_4).
- **2.1.x stream (cross-stream)**: versions 2.1.0 and 2.1.1 are also affected. This will be reported as cross-stream impact (Step 7, Case B).
- The fix was picked up in the 2.2.x stream starting with version 2.2.3 (build 0.4.11, 2026-03-23). No new remediation is needed for 2.2.3+.
- For affected 2.2.x versions (2.2.0-2.2.2), the fix is already available in the stream -- versions 2.2.3+ ship it. If these older versions need z-stream respins, the rpms.lock.yaml must be updated.
