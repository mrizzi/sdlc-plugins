# Step 2 -- Version Impact Analysis

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| RHTPA 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| RHTPA 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| RHTPA 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| RHTPA 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| RHTPA 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as RHTPA 2.2.1; carries forward 0.11.12) |
| RHTPA 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | 0.11.14 is the fixed version |
| RHTPA 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | 0.11.14 is the fixed version |

## Evidence

All version determinations are based on the mock lock file data (pinned commit tags from the supportability matrix, per Important Rule 13):

- **v0.3.8** (RHTPA 2.1.0): quinn-proto 0.11.9 -- AFFECTED (< 0.11.14)
- **v0.3.12** (RHTPA 2.1.1): quinn-proto 0.11.9 -- AFFECTED (< 0.11.14)
- **v0.4.5** (RHTPA 2.2.0): quinn-proto 0.11.9 -- AFFECTED (< 0.11.14)
- **v0.4.8** (RHTPA 2.2.1): quinn-proto 0.11.12 -- AFFECTED (< 0.11.14)
- **v0.4.9** (RHTPA 2.2.2): retag of v0.4.8 -- lock file check skipped, carries forward AFFECTED status from RHTPA 2.2.1
- **v0.4.11** (RHTPA 2.2.3): quinn-proto 0.11.14 -- NOT AFFECTED (fixed version)
- **v0.4.12** (RHTPA 2.2.4): quinn-proto 0.11.14 -- NOT AFFECTED (fixed version)

## Upstream Fix Status

| Stream | Ecosystem | Repository | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|------------|-----------------|-----------------|--------|
| 2.1.x | Cargo | backend | release/0.3.z | Unknown (latest released tag v0.3.12 has 0.11.9) | Likely NO |
| 2.2.x | Cargo | backend | release/0.4.z | 0.11.14 (based on latest tags v0.4.11/v0.4.12) | YES |

The 2.2.x upstream branch (release/0.4.z) already has the fix at the latest released tags (v0.4.11+), indicating the upstream fix has already landed on that branch. The 2.1.x upstream branch (release/0.3.z) still shows 0.11.9 at its latest released tag (v0.3.12), indicating the fix has not been backported to that branch.

## Cross-Stream Impact Summary

- **2.1.x stream**: ALL versions affected (RHTPA 2.1.0, RHTPA 2.1.1) -- this is outside the issue's stream scope [rhtpa-2.2] but is noted for cross-stream impact awareness (Case B).
- **2.2.x stream**: RHTPA 2.2.0, 2.2.1, and 2.2.2 are affected. RHTPA 2.2.3 and 2.2.4 are NOT affected (already ship fixed version 0.11.14).
