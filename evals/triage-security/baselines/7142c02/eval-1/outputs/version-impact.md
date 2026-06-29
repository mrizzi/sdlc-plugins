# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Fix Threshold

quinn-proto < 0.11.14 is vulnerable. Fixed version: 0.11.14.

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | ships fixed version |

## Summary by Stream

| Stream | Affected Versions | Unaffected Versions |
|--------|-------------------|---------------------|
| 2.1.x | 2.1.0, 2.1.1 | (none) |
| 2.2.x | 2.2.0, 2.2.1, 2.2.2 | 2.2.3, 2.2.4 |

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  Ecosystem: Cargo (Rust crate)
  Lock file: Cargo.lock
  Repository: backend

  quinn-proto is a QUIC protocol implementation crate.
  Present in all versions across both streams (2.1.x and 2.2.x).

  Stream 2.1.x: quinn-proto 0.11.9 in all versions (v0.3.8, v0.3.12) -- AFFECTED
  Stream 2.2.x: quinn-proto 0.11.9 (v0.4.5), 0.11.12 (v0.4.8/v0.4.9), 0.11.14 (v0.4.11+)
    Versions 2.2.0-2.2.2 AFFECTED, versions 2.2.3+ ship the fix.
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Available? | Notes |
|--------|-----------|-----------------|----------------|-------|
| 2.1.x | Cargo | `release/0.3.z` | Unknown | Needs `git show` verification at branch HEAD |
| 2.2.x | Cargo | `release/0.4.z` | YES | v0.4.11 and v0.4.12 already ship 0.11.14 |

For the 2.2.x stream, the fix was incorporated starting with build 0.4.11 (version 2.2.3). The upstream branch `release/0.4.z` already has the fix based on the latest released versions (v0.4.11, v0.4.12 both ship quinn-proto 0.11.14).

For the 2.1.x stream, the latest build tag `v0.3.12` still ships quinn-proto 0.11.9. The upstream branch `release/0.3.z` status would need to be verified via `git show`.
