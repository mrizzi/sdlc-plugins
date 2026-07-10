# Step 2 — Version Impact Analysis: CVE-2026-48901

## Enriched Fix Threshold

From Step 1.5 cross-validation: **h2 < 0.4.8 is affected** (fix threshold: 0.4.8)

## Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

| Stream | Version | Backend Tag | h2 version | Affected? | Notes |
|--------|---------|-------------|------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.x | 2.1.1 | v0.3.12 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.x | 2.2.0 | v0.4.5 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (fixed) |
| 2.2.x | 2.2.1 | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (fixed) |
| 2.2.x | 2.2.2 | v0.4.8 | — | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 (fixed) |
| 2.2.x | 2.2.4 | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 (fixed) |

## Impact Summary

- **Stream 2.1.x**: ALL versions affected (2.1.0, 2.1.1 ship h2 0.4.5)
- **Stream 2.2.x**: NO versions affected (all versions ship h2 >= 0.4.8)

## Issue Scope Analysis

- Issue TC-8030 is **scoped to stream 2.2.x** (suffix `[rhtpa-2.2]`)
- **No versions in the scoped stream (2.2.x) are affected**
- **Cross-stream impact**: stream 2.1.x IS affected (all versions ship h2 0.4.5 < 0.4.8)

## Dependency Chain Context

Dependency chain for h2 (Cargo):

```
backend (workspace) -> ... -> h2
Ecosystem: Cargo (crates.io)
Lock file: Cargo.lock
Profile: production (h2 is an HTTP/2 runtime dependency)
```

For affected versions (2.1.x stream):
- h2 0.4.5 is present in Cargo.lock at tags v0.3.8 and v0.3.12
- h2 was already updated to 0.4.8 (the fixed version) starting from tag v0.4.5 (2.2.0)
- The fix was introduced between the 2.1.x and 2.2.x streams

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.1.x | Cargo | release/0.3.z | Upstream fix PR: hyperium/h2#800 |
| 2.2.x | Cargo | release/0.4.z | Already ships fixed h2 >= 0.4.8 |

## Triage Outcome Determination

1. **Any supported versions affected?** YES (2.1.x versions are affected)
2. **Issue scoped to a single stream?** YES (scoped to 2.2.x)
3. **Scoped stream affected?** NO (all 2.2.x versions ship h2 >= 0.4.8)
4. **Other streams affected?** YES (2.1.x is affected)

This means:
- **For TC-8030 (scoped to 2.2.x)**: Recommend close as Not a Bug — no versions in the 2.2.x stream ship a vulnerable version of h2. All 2.2.x versions ship h2 >= 0.4.8 which is at or above the fix threshold.
- **Cross-stream impact (Case B)**: Post cross-stream impact comment noting that stream 2.1.x is affected. Create preemptive remediation tasks for 2.1.x if no CVE Jira exists for that stream.
