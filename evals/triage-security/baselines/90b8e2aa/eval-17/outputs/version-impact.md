# Step 2 -- Version Impact Analysis

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Build Tag | quinn-proto | Affected? | Notes |
|--------|---------|-----------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Dependency Chain Context

```
Dependency chain for quinn-proto (Cargo):
  Ecosystem: Cargo (Rust crate)
  Lock file: Cargo.lock
  Repository: backend

  quinn-proto is a QUIC transport protocol implementation crate.
  Present in Cargo.lock at pinned source commits for all versions.

  First appeared: present in all checked versions (2.1.0 onward)
  Fixed in: 2.2.3 (v0.4.11) where quinn-proto was bumped to 0.11.14
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD (v0.4.12) | Fixed? |
|--------|-----------|-----------------|---------------------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |

The upstream branch `release/0.4.z` already ships quinn-proto 0.11.14, which is the fixed version. Remediation for affected 2.2.x versions involves updating the source tag reference in the Konflux release repo to pick up the fix that is already present in later builds.

## Cross-Stream Impact Summary

The issue is scoped to stream **2.2.x** (per summary suffix `[rhtpa-2.2]`).

However, the version impact analysis reveals that **stream 2.1.x is also affected**:
- 2.1.0 ships quinn-proto 0.11.9 (affected)
- 2.1.1 ships quinn-proto 0.11.9 (affected)

This cross-stream impact triggers **Case B** in Step 8: a cross-stream impact comment should be posted, and proactive remediation may be needed for the 2.1.x stream if no companion CVE Jira exists for that stream.

## Stream-Scoped Summary (2.2.x only)

Within the issue's scope (2.2.x stream):
- **Affected versions**: 2.2.0, 2.2.1, 2.2.2
- **Not affected versions**: 2.2.3, 2.2.4 (ship fixed quinn-proto 0.11.14)
- **Fix already present in stream**: yes, from version 2.2.3 onward
