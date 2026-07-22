# Step 2 -- Version Impact Analysis

## Enriched Fix Threshold

Using the enriched fix threshold from Step 1.5:
- **Affected range**: h2 < 0.4.8
- **Fix version**: h2 0.4.8
- **Source**: MITRE CVE API + OSV.dev (cross-validated)

## Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

| Stream | Version | Build Tag | h2 version | Affected? | Notes |
|--------|---------|-----------|------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.x | 2.1.1 | v0.3.12 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.x | 2.2.0 | v0.4.5 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.x | 2.2.1 | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 |
| 2.2.x | 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.4.9 | NO | 0.4.9 > 0.4.8 |
| 2.2.x | 2.2.4 | v0.4.12 | 0.4.9 | NO | 0.4.9 > 0.4.8 |

## Impact Summary by Stream

| Stream | Affected Versions | Not Affected Versions |
|--------|-------------------|-----------------------|
| 2.1.x | 2.1.0, 2.1.1 (all) | -- |
| 2.2.x | -- | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 (all) |

## Issue Scope Analysis

This issue is **scoped to stream 2.2.x** (suffix `[rhtpa-2.2]`).

- **2.2.x stream (issue scope)**: NO versions affected. All versions in the 2.2.x
  stream ship h2 >= 0.4.8, which is at or above the fix threshold.
- **2.1.x stream (outside issue scope)**: ALL versions affected. Both 2.1.0 and
  2.1.1 ship h2 0.4.5, which is below the fix threshold of 0.4.8.

## Dependency Chain Context

Dependency chain for h2:
- Ecosystem: Cargo (Rust crate, crates.io)
- Lock file: Cargo.lock
- Type: source dependency (requires upstream backport + downstream propagation for remediation)

## Cross-Stream Observation

While the 2.2.x stream (issue scope) is not affected, the 2.1.x stream IS affected.
This is relevant for Case B (cross-stream impact) and preemptive remediation
in Step 8.
