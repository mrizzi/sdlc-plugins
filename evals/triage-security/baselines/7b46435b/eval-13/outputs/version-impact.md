# Step 2 -- Version Impact Analysis for CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8, quinn-proto 0.11.12) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Dependency Chain Context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) -> quinn-proto 
  Ecosystem: Cargo (source dependency in Cargo.lock)

  Versions 2.2.0-2.2.2 ship quinn-proto < 0.11.14 (vulnerable)
  Versions 2.2.3-2.2.4 ship quinn-proto 0.11.14 (fixed)
  Versions 2.1.0-2.1.1 ship quinn-proto 0.11.9 (vulnerable)
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Build Tag | Version at Tag | Fixed? |
|--------|-----------|-----------------|------------------|----------------|--------|
| 2.1.x | Cargo | release/0.3.z | v0.3.12 | 0.11.9 | NO |
| 2.2.x | Cargo | release/0.4.z | v0.4.12 | 0.11.14 | YES |

The 2.2.x stream already ships the fix in versions 2.2.3+ (quinn-proto 0.11.14). The 2.1.x stream does NOT have the fix -- all versions ship quinn-proto 0.11.9.

## Affects Versions Correction (Step 3)

The issue is scoped to the 2.2.x stream. Only versions from the 2.2.x stream are included in the Affects Versions correction.

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

RHTPA 2.0.0 does not exist in any configured version stream. The correct Affects Versions for the 2.2.x stream are RHTPA 2.2.0, RHTPA 2.2.1, and RHTPA 2.2.2 (all ship quinn-proto < 0.11.14). Versions 2.2.3 and 2.2.4 are excluded because they already ship quinn-proto 0.11.14 (the fixed version).

## Cross-Stream Impact Summary

The 2.1.x stream (outside the issue's scope) is also affected:
- 2.1.0 ships quinn-proto 0.11.9 (affected)
- 2.1.1 ships quinn-proto 0.11.9 (affected)
- The upstream branch release/0.3.z does not have the fix

This triggers Case B (cross-stream impact) in Step 8. Since no CVE Jira exists for the 2.1.x stream, preemptive remediation tasks will be created.
