# Step 2 -- Version Impact Analysis

## Stream Scope

This issue is scoped to the **2.2.x** stream (from summary suffix `[rhtpa-2.2]`).

## Supportability Matrix (2.2.x stream)

Source: rhtpa-release.0.4.z security-matrix.md

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## RPM Lock File Extraction (rpms.lock.yaml)

Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`

| Version | Tag | openssl-libs version (rpms.lock.yaml) | Affected? | Notes |
|---------|-----|---------------------------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 (fix threshold) |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 (fix threshold) |
| 2.2.2 | v0.4.9 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | = 3.0.7-28.el9_4 (at fix threshold) |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | = 3.0.7-28.el9_4 (at fix threshold) |

## Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 |
| 2.2.3 | 3.0.7-28.el9_4 | NO | at fix threshold |
| 2.2.4 | 3.0.7-28.el9_4 | NO | at fix threshold |

## Cross-stream Impact (out of scope, informational only)

The 2.1.x stream is NOT within this issue's scope but is also affected for informational purposes:

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 3.0.7-24.el9 | YES | |
| 2.1.1 | 3.0.7-24.el9 | YES | |

The 2.1.x stream is tracked separately. If no companion CVE Jira exists for the 2.1.x stream, preemptive remediation tasks would be created per Case B.

## Summary

- **Affected versions (2.2.x stream)**: 2.2.0, 2.2.1, 2.2.2
- **Not affected versions (2.2.x stream)**: 2.2.3, 2.2.4
- **Fix threshold**: openssl-libs 3.0.7-28.el9_4 (versions at or above this are not affected)
- **Ecosystem**: RPM -- remediation is a single Konflux release repo task (no upstream backport needed)
