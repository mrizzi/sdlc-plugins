# Step 2 -- Version Impact Analysis for CVE-2026-31812

## Fix Threshold

- **Library**: quinn-proto
- **Affected range**: versions before 0.11.14 (< 0.11.14)
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
Dependency chain for quinn-proto (Cargo):
  backend (workspace) -> quinn -> quinn-proto
  Ecosystem: Cargo
  Lock file: Cargo.lock
  Profile: production (runtime dependency)

  Present in all versions across both streams (2.1.x and 2.2.x).
  The fix was picked up starting at build tag v0.4.11 (version 2.2.3).
```

## Stream-Scoped Impact Summary

This issue is scoped to stream **2.2.x** (per summary suffix `[rhtpa-2.2]`).

**Within 2.2.x scope:**
- **Affected**: 2.2.0, 2.2.1, 2.2.2 (ship quinn-proto 0.11.9 or 0.11.12, both < 0.11.14)
- **Not affected**: 2.2.3, 2.2.4 (ship quinn-proto 0.11.14, the fixed version)

**Outside scope (2.1.x stream -- tracked by companion issue):**
- 2.1.0 and 2.1.1 are also affected (quinn-proto 0.11.9), but belong to stream 2.1.x and are tracked by a separate PSIRT-created Vulnerability issue for that stream.

## Cross-Stream Impact

The 2.1.x stream is also affected (2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). Since this issue is scoped to 2.2.x, the 2.1.x impact is reported as a cross-stream notice per Case B of Step 7.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Source Repo | Notes |
|--------|-----------|-----------------|-------------|-------|
| 2.2.x | Cargo | release/0.4.z | backend | Fix already present -- v0.4.11+ ships 0.11.14 |
| 2.1.x | Cargo | release/0.3.z | backend | Fix NOT present -- latest (v0.3.12) ships 0.11.9 |

The upstream fix (quinn-proto bump to 0.11.14) is already present on the release/0.4.z branch (as evidenced by builds v0.4.11 and v0.4.12). However, the fix has NOT been backported to release/0.3.z (the 2.1.x branch).

## Affects Versions Correction Needed

Current PSIRT-assigned Affects Versions: `RHTPA 2.0.0`
This is incorrect -- there is no 2.0.x stream. Based on lock file analysis scoped to stream 2.2.x:

Proposed correction: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are NOT affected (they ship the fixed quinn-proto 0.11.14).
