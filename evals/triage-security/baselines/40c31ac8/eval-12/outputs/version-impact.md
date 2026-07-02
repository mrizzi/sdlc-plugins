# Step 2 -- Version Impact Analysis

## Enriched Fix Threshold

From Step 1.5 cross-validation: h2 **< 0.4.8** is affected. Versions >= 0.4.8 are not affected.

## Version Impact Table for CVE-2026-48901 (h2 < 0.4.8)

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.1.1 | v0.3.12 | 0.4.5 | YES | 0.4.5 < 0.4.8 |

### Stream 2.2.x (rhtpa-release.0.4.z) -- issue scope

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.1 | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 |
| 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.4.9 | NO | 0.4.9 > 0.4.8 |
| 2.2.4 | v0.4.12 | 0.4.9 | NO | 0.4.9 > 0.4.8 |

### Combined Impact Summary

| Stream | Versions Affected | Versions Not Affected |
|--------|-------------------|-----------------------|
| 2.1.x | 2.1.0, 2.1.1 | -- |
| 2.2.x (issue scope) | -- | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 |

## Findings

- **Within the issue's stream scope (2.2.x): NO versions are affected.** All 2.2.x product versions ship h2 >= 0.4.8 (the fix threshold). The earliest 2.2.x release (2.2.0, build tag v0.4.5) already includes h2 0.4.8.
- **Cross-stream impact (2.1.x): ALL versions are affected.** Both 2.1.0 and 2.1.1 ship h2 0.4.5, which is below the fix threshold of 0.4.8. The 2.1.x stream uses build tags v0.3.8 and v0.3.12 which both pin h2 at 0.4.5.

## Triage Outcome

This is a **Case C** scenario for the 2.2.x stream: no supported versions within the issue's scope ship a vulnerable version of h2. All 2.2.x versions ship h2 0.4.8 or later, which is at or above the fix threshold.

**Cross-stream impact (Case B)**: The 2.1.x stream IS affected (both versions ship h2 0.4.5 < 0.4.8). This should be flagged for companion issue tracking or preemptive remediation if no sibling CVE Jira exists for the 2.1.x stream.

**Recommendation**: Close TC-8030 as Not a Bug -- the 2.2.x stream is not affected by CVE-2026-48901. Post cross-stream impact notice for the 2.1.x stream.
