# Step 2 -- Version Impact Analysis for TC-8001

## CVE Details

- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Affected range**: versions before 0.11.14
- **Fixed version**: 0.11.14

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (Cargo)
  Profile: production (quinn-proto is a runtime dependency for QUIC transport)
  Ecosystem: Cargo
  Lock file: Cargo.lock
```

quinn-proto is present across all checked versions in both streams. The fix was introduced at tag v0.4.11 (version 2.2.3) in the 2.2.x stream. The 2.1.x stream has no version shipping the fix.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fixed at branch HEAD? | Notes |
|--------|-----------|-----------------|----------------------|-------|
| 2.1.x | Cargo | release/0.3.z | Unknown (would require git show) | All released versions ship 0.11.9 |
| 2.2.x | Cargo | release/0.4.z | YES | v0.4.11+ ships 0.11.14 (fixed) |

## Affects Versions Correction Needed

The Jira issue currently has **Affects Versions: RHTPA 2.0.0**, but there is no 2.0.x stream configured. Based on the version impact analysis:

- **Scoped stream (2.2.x)**: Affected versions are RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Cross-stream (2.1.x)**: Affected versions are RHTPA 2.1.0, RHTPA 2.1.1

The Affects Versions field should be corrected to: **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2** (scoped to the 2.2.x stream per the issue's stream suffix).

RHTPA 2.0.0 should be removed -- it does not correspond to any configured version stream and is incorrect.

## Summary

- **2.2.x stream (issue scope)**: 3 of 5 versions affected (2.2.0, 2.2.1, 2.2.2). Fix landed in 2.2.3 (tag v0.4.11).
- **2.1.x stream (cross-stream)**: All 2 versions affected (2.1.0, 2.1.1). No version in this stream ships the fix.
- **Remediation path**: Cargo source dependency -- requires upstream backport task + downstream propagation subtask per affected stream.
