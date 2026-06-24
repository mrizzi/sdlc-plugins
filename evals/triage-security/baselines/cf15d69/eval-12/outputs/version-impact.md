# Step 2 -- Version Impact Analysis

## Enriched Fix Threshold

From Step 1.5 cross-validation: h2 < **0.4.8** is affected. Versions shipping h2 >= 0.4.8 are NOT affected.

## Stream Scope

This issue is scoped to stream **2.2.x** (suffix `[rhtpa-2.2]`). The version impact table below covers only the 2.2.x stream for Affects Versions purposes, but the full analysis across all streams is included for cross-stream impact assessment.

## Version Impact Table

### Stream 2.1.x (rhtpa-release.0.3.z) -- outside issue scope, for cross-stream reference

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.1 | v0.3.12 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |

### Stream 2.2.x (rhtpa-release.0.4.z) -- issue scope

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.4.8 | **NO** | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.1 | v0.4.8 | 0.4.8 | **NO** | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.2 | v0.4.9 | -- | **NO** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.4.9 | **NO** | 0.4.9 >= 0.4.8 |
| 2.2.4 | v0.4.12 | 0.4.9 | **NO** | 0.4.9 >= 0.4.8 |

## Summary

### In-scope stream (2.2.x)

**No versions in the 2.2.x stream are affected.** All 2.2.x versions ship h2 >= 0.4.8, which is at or above the fix threshold. The earliest 2.2.x version (2.2.0, build v0.4.5) already ships h2 0.4.8.

### Cross-stream impact (2.1.x)

**Both versions in the 2.1.x stream are affected.** Versions 2.1.0 and 2.1.1 ship h2 0.4.5, which is below the fix threshold of 0.4.8. This is outside the current issue's scope but is noted for cross-stream coordination (Step 4 / Case B).

## Recommendation

For the scoped stream (2.2.x): **Close as Not a Bug** -- no supported 2.2.x versions ship a vulnerable version of h2. All versions ship h2 >= 0.4.8 which is at or above the fix threshold.

Cross-stream: The 2.1.x stream IS affected (h2 0.4.5 < 0.4.8). This should be flagged for cross-stream coordination -- a companion CVE issue for the 2.1.x stream may need remediation.
