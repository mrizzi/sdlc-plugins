# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Build Tag | quinn-proto | Affected? | Notes |
|--------|---------|-----------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8, quinn-proto 0.11.12) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1) -- both ship quinn-proto 0.11.9
- **2.2.x stream**: versions 2.2.0, 2.2.1, 2.2.2 affected; versions 2.2.3 and 2.2.4 already ship the fix (0.11.14)

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) -> quinn-proto (via QUIC transport dependency chain)
  Ecosystem: Cargo (Cargo.lock)
  Lock file: Cargo.lock
  Profile: production (runtime dependency)

  First seen at vulnerable version: all versions from 2.1.0 onward
  Fixed starting from: 2.2.3 (build v0.4.11, quinn-proto bumped to 0.11.14)
```

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD (v0.4.12) | Fixed? |
|--------|-----------|-----------------|---------------------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 | NO |

- **2.2.x stream (release/0.4.z)**: The upstream branch already has the fix at the latest tag (v0.4.12 ships quinn-proto 0.11.14). Versions 2.2.3+ already include it. Remediation for 2.2.0-2.2.2 requires a downstream propagation to reference a tag >= v0.4.11.
- **2.1.x stream (release/0.3.z)**: The upstream branch still ships quinn-proto 0.11.9 at the latest tag (v0.3.12). Remediation requires an upstream backport to bump quinn-proto on the release/0.3.z branch first, followed by a downstream propagation.

## Scoped vs Cross-Stream Impact

This issue is scoped to the **2.2.x** stream (per the `[rhtpa-2.2]` suffix).

- **In-scope (2.2.x)**: Versions 2.2.0, 2.2.1, 2.2.2 are affected -- Case A remediation applies.
- **Cross-stream (2.1.x)**: Versions 2.1.0, 2.1.1 are also affected -- Case B cross-stream impact applies. Preemptive remediation tasks should be created for the 2.1.x stream if no sibling CVE Jira exists for that stream.
