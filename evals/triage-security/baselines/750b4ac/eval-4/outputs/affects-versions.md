# Step 3 -- Affects Versions Correction

## Current Affects Versions (from Jira)

- RHTPA 2.1.0
- RHTPA 2.2.0

## Version Impact Evidence

Based on lock file analysis (Step 2), the actual impact is:

| Version | h2 version | Affected? |
|---------|------------|-----------|
| RHTPA 2.1.0 | 0.4.5 | YES |
| RHTPA 2.1.1 | 0.4.5 | YES |
| RHTPA 2.2.0 | 0.4.8 | NO |
| RHTPA 2.2.1 | 0.4.8 | NO |
| RHTPA 2.2.2 | 0.4.8 | NO |
| RHTPA 2.2.3 | 0.4.9 | NO |
| RHTPA 2.2.4 | 0.4.9 | NO |

## Proposed Affects Versions

- **RHTPA 2.1.0** (keep -- affected, h2 0.4.5 < 0.4.8)
- **RHTPA 2.1.1** (add -- affected, h2 0.4.5 < 0.4.8)

## Changes

| Action | Version | Reason |
|--------|---------|--------|
| Keep | RHTPA 2.1.0 | Ships h2 0.4.5, within affected range (< 0.4.8) |
| Add | RHTPA 2.1.1 | Ships h2 0.4.5, within affected range (< 0.4.8) -- was missing from PSIRT assignment |
| Remove | RHTPA 2.2.0 | Ships h2 0.4.8, at or above fixed version -- NOT affected |

## Rationale

This issue is UNSCOPED (no stream suffix in the summary), so Affects Versions should include only the versions that are actually affected across all streams. PSIRT included RHTPA 2.2.0 based on scan-time scope, but lock file evidence shows RHTPA 2.2.0 ships h2 0.4.8 (the fixed version itself) and is not vulnerable. PSIRT also missed RHTPA 2.1.1, which ships the same vulnerable h2 0.4.5 as RHTPA 2.1.0.

The corrected Affects Versions list includes only the two 2.1.x versions that actually ship the vulnerable dependency.
