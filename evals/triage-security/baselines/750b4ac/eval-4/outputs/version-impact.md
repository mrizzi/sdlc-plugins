# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-33501 (h2 < 0.4.8)

**Overall result: MIXED** -- 2.1.x stream is affected, 2.2.x stream is NOT affected.

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| RHTPA 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | YES | < 0.4.8 |
| RHTPA 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | YES | < 0.4.8 |
| RHTPA 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | >= 0.4.8 (fixed version) |
| RHTPA 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | >= 0.4.8 (fixed version) |
| RHTPA 2.2.2 | 2.2.x | v0.4.9 | 0.4.8 | NO | retag of RHTPA 2.2.1 (same as 2.2.1) |
| RHTPA 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | >= 0.4.8 |
| RHTPA 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | >= 0.4.8 |

## Stream Summary

| Stream | Affected? | Reason |
|--------|-----------|--------|
| 2.1.x | YES | All versions ship h2 0.4.5 (< 0.4.8) |
| 2.2.x | NO | All versions ship h2 >= 0.4.8 (at or above the fixed version) |

## Dependency Chain Context

The h2 crate is a Cargo (source) dependency in the backend repository. It is used for HTTP/2 protocol support. The 2.1.x stream pins backend source at tags v0.3.8 and v0.3.12, both of which include h2 0.4.5 in their Cargo.lock. The 2.2.x stream upgraded h2 to 0.4.8+ starting from its first release (RHTPA 2.2.0, tag v0.4.5).

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | Needs backport -- h2 must be bumped to >= 0.4.8 |
| 2.2.x | Cargo | release/0.4.z | Already fixed -- h2 >= 0.4.8 at branch HEAD |
