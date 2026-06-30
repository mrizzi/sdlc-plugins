# Step 2 -- Version Impact Analysis

## Stream Scope

Triage is scoped to the **2.2.x** stream (Konflux release repo: `rhtpa-release.0.4.z`).

## Supportability Matrix (2.2.x stream)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## Dependency Version Extraction (rpms.lock.yaml)

CVE-2026-40215 affects openssl-libs versions **before 3.0.7-28.el9_4**. The fixed version is **3.0.7-28.el9_4**.

| Version | Tag | openssl-libs version (rpms.lock.yaml) | Affected? | Notes |
|---------|-----|---------------------------------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | `v0.4.8` | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | `v0.4.9` | -- | YES | retag of 2.2.1 (same as 2.2.1: 3.0.7-27.el9_4) |
| 2.2.3 | `v0.4.11` | 3.0.7-28.el9_4 | NO | = 3.0.7-28.el9_4 (fixed version) |
| 2.2.4 | `v0.4.12` | 3.0.7-28.el9_4 | NO | = 3.0.7-28.el9_4 (fixed version) |

## Summary

Versions **2.2.0, 2.2.1, and 2.2.2** ship a vulnerable version of openssl-libs (before 3.0.7-28.el9_4).

Versions **2.2.3 and 2.2.4** ship the fixed version (3.0.7-28.el9_4) and are NOT affected.

## Dependency Chain Context

See `sbom-verification.md` for the full SBOM verification results and dependency chain analysis for the affected versions.
