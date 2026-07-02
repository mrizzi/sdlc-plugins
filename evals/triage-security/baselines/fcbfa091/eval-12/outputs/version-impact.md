# Step 2 -- Version Impact Analysis

## Fix Threshold

Using enriched fix threshold from Step 1.5: **h2 < 0.4.8** (versions strictly less than 0.4.8 are affected).

This threshold was cross-validated by MITRE CVE API (lessThan 0.4.8) and OSV.dev (fixed 0.4.8). The imprecise Jira description ("versions prior to the fix") was not used for version comparisons.

## Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

| Version | Stream | Backend Tag | h2 version | Affected? | Notes |
|---------|--------|-------------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix version) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix version) |
| 2.2.2 | 2.2.x | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

## Stream Impact Summary

| Stream | Affected Versions | Status |
|--------|-------------------|--------|
| 2.1.x | 2.1.0, 2.1.1 | AFFECTED -- all versions ship h2 0.4.5 (< 0.4.8) |
| 2.2.x (scoped) | None | NOT AFFECTED -- all versions ship h2 >= 0.4.8 |

## Dependency Chain Context

```
Dependency chain for h2 (Cargo):
  Ecosystem: Cargo (crates.io)
  Lock file: Cargo.lock
  Repository: backend

  Stream 2.1.x: h2 0.4.5 at both v0.3.8 and v0.3.12
  Stream 2.2.x: h2 0.4.8 from v0.4.5 onward (at or above fix threshold)
```

## Scoped Stream Assessment

This issue is scoped to stream **2.2.x** (from the `[rhtpa-2.2]` suffix). Within the 2.2.x stream, **no versions are affected** -- all versions ship h2 >= 0.4.8, which is at or above the fix threshold.

## Cross-Stream Impact

Stream **2.1.x** (outside the issue's scope) IS affected -- all 2.1.x versions (2.1.0 and 2.1.1) ship h2 0.4.5, which is below the fix threshold of 0.4.8. This cross-stream impact is addressed in the remediation step.
