# Step 2 -- Version Impact Analysis

## Enriched Fix Threshold

From Step 1.5 cross-validation: **h2 < 0.4.8 is affected, h2 >= 0.4.8 is not affected.**

Both MITRE CVE API and OSV.dev agree on this threshold. The Jira description was
imprecise ("versions prior to the fix") and could not be used alone.

## Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

### Stream 2.2.x (scoped stream -- issue suffix [rhtpa-2.2])

| Version | Build | Backend Tag | h2 Version | Affected? | Notes |
|---------|-------|-------------|------------|-----------|-------|
| 2.2.0 | 0.4.5 | v0.4.5 | 0.4.8 | NO | h2 0.4.8 >= 0.4.8 (at or above fix threshold) |
| 2.2.1 | 0.4.8 | v0.4.8 | 0.4.8 | NO | h2 0.4.8 >= 0.4.8 (at or above fix threshold) |
| 2.2.2 | 0.4.9 | v0.4.8 | 0.4.8 | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.11 | v0.4.11 | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 (above fix threshold) |
| 2.2.4 | 0.4.12 | v0.4.12 | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 (above fix threshold) |

**Result: No versions in the scoped stream 2.2.x are affected.** All versions ship
h2 >= 0.4.8, which is at or above the fix threshold.

### Stream 2.1.x (cross-stream analysis)

| Version | Build | Backend Tag | h2 Version | Affected? | Notes |
|---------|-------|-------------|------------|-----------|-------|
| 2.1.0 | 0.3.8 | v0.3.8 | 0.4.5 | YES | h2 0.4.5 < 0.4.8 (below fix threshold) |
| 2.1.1 | 0.3.12 | v0.3.12 | 0.4.5 | YES | h2 0.4.5 < 0.4.8 (below fix threshold) |

**Result: All versions in stream 2.1.x are affected.** Both versions ship h2 0.4.5,
which is below the fix threshold of 0.4.8.

## Summary

| Stream | Versions Affected | Versions Not Affected |
|--------|-------------------|-----------------------|
| 2.2.x (scoped) | 0 of 5 | 5 of 5 |
| 2.1.x (cross-stream) | 2 of 2 | 0 of 2 |

## Triage Outcome

**Scoped stream (2.2.x): Case C -- No supported versions affected.** All 2.2.x
versions ship h2 >= 0.4.8, which is at or above the fix threshold. Recommendation
is to close TC-8030 as Not a Bug (not affected).

**Cross-stream impact (2.1.x): Case B -- Other streams affected.** Stream 2.1.x
ships h2 0.4.5 in all versions, which is below the fix threshold. Cross-stream
impact should be noted, and preemptive remediation tasks should be created for
stream 2.1.x if no companion CVE Jira exists for that stream.
