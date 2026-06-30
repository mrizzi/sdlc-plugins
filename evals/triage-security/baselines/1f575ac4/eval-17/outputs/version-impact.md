# Step 2 -- Version Impact Analysis

## Version Impact Table

CVE-2026-31812 affects quinn-proto versions before 0.11.14. Fixed version: 0.11.14.

| Stream | Version | Build Tag | quinn-proto version | Affected? | Notes |
|--------|---------|-----------|---------------------|-----------|-------|
| 2.1.x | 2.1.0 | `v0.3.8` | 0.11.9 | YES | < 0.11.14 |
| 2.1.x | 2.1.1 | `v0.3.12` | 0.11.9 | YES | < 0.11.14 |
| 2.2.x | 2.2.0 | `v0.4.5` | 0.11.9 | YES | < 0.11.14 |
| 2.2.x | 2.2.1 | `v0.4.8` | 0.11.12 | YES | < 0.11.14 |
| 2.2.x | 2.2.2 | `v0.4.9` | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | `v0.4.11` | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.x | 2.2.4 | `v0.4.12` | 0.11.14 | NO | >= 0.11.14 (fixed) |

## Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1) -- quinn-proto 0.11.9 is below fix threshold 0.11.14
- **2.2.x stream**: versions 2.2.0, 2.2.1, 2.2.2 are affected; versions 2.2.3 and 2.2.4 are NOT affected (ship quinn-proto 0.11.14, the fixed version)

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto (Cargo):
  Ecosystem: Cargo (Rust crate)
  Lock file: Cargo.lock
  quinn-proto is a QUIC protocol implementation crate

  The dependency is present in all versions across both streams.
  First appeared: 2.1.0 (v0.3.8) with quinn-proto 0.11.9
  Fixed from: 2.2.3 (v0.4.11) with quinn-proto 0.11.14
```

## Upstream Fix Status (Step 2.5)

The upstream fix PR is [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048).

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.1.x | Cargo | `release/0.3.z` | Needs verification at branch HEAD |
| 2.2.x | Cargo | `release/0.4.z` | Fixed from v0.4.11 onward (quinn-proto 0.11.14) |

The 2.2.x stream is already fixed in versions 2.2.3+ (build tags v0.4.11, v0.4.12 ship quinn-proto 0.11.14). The 2.1.x stream remains affected in all released versions.

## Cross-Stream Impact

This issue is scoped to **2.2.x** (from summary suffix `[rhtpa-2.2]`). However, the 2.1.x stream is also affected:
- 2.1.0 ships quinn-proto 0.11.9 (affected)
- 2.1.1 ships quinn-proto 0.11.9 (affected)

This triggers **Case B** (cross-stream impact) in Step 7 for the 2.1.x stream.

## Affects Versions Correction (Step 3)

The Jira issue currently has `Affects Versions: RHTPA 2.0.0`. Based on version impact analysis:

- `RHTPA 2.0.0` is **incorrect** -- no 2.0.x stream exists in the configuration
- Within the scoped 2.2.x stream, affected versions are: **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2**
- Versions 2.2.3 and 2.2.4 are NOT affected (ship fixed quinn-proto 0.11.14)

**Proposed correction**: Remove `RHTPA 2.0.0`, add `RHTPA 2.2.0`, `RHTPA 2.2.1`, `RHTPA 2.2.2`.
