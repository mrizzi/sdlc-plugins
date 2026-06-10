# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-33501 (h2 < 0.4.8)

### Stream 1: rhtpa-release.0.3.z (2.1.x stream)

| Version | Build | Build Date | Pinned Tag | h2 version | Affected? | Notes |
|---------|-------|------------|------------|------------|-----------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 | 0.4.5 | YES | < 0.4.8 |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 | 0.4.5 | YES | < 0.4.8 |

### Stream 2: rhtpa-release.0.4.z (2.2.x stream)

| Version | Build | Build Date | Pinned Tag | h2 version | Affected? | Notes |
|---------|-------|------------|------------|------------|-----------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | 0.4.9 | NO | >= 0.4.8 (fixed) |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | 0.4.9 | NO | >= 0.4.8 (fixed) |

### Combined Version Impact Table

| Version | Stream | h2 version | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.4.5 | YES | < 0.4.8 |
| 2.1.1 | 2.1.x | 0.4.5 | YES | < 0.4.8 |
| 2.2.0 | 2.2.x | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.1 | 2.2.x | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.4.9 | NO | >= 0.4.8 (fixed) |
| 2.2.4 | 2.2.x | 0.4.9 | NO | >= 0.4.8 (fixed) |

## Mixed Impact Summary

This CVE has **mixed impact** across streams:

- **2.1.x stream**: ALL versions affected (h2 0.4.5, which is < 0.4.8)
- **2.2.x stream**: NO versions affected (all ship h2 >= 0.4.8)

The 2.2.x stream already ships the fixed version of h2 (0.4.8+) starting from its earliest release (2.2.0). Remediation is required **only** for the 2.1.x stream.

## Dependency Chain Context

```
Dependency chain for h2 (Cargo):
  rhtpa-backend (workspace) -> [intermediary crates] -> h2
  Ecosystem: Cargo (Rust crate)
  
  2.1.x stream (v0.3.8, v0.3.12): h2 0.4.5 -- VULNERABLE
  2.2.x stream (v0.4.5+): h2 0.4.8+ -- FIXED
```

The h2 crate handles HTTP/2 framing. The vulnerability (memory exhaustion via CONTINUATION frames) is exploitable when a peer sends excessive CONTINUATION frames, leading to unbounded memory allocation.

## Upstream Fix Status

The upstream fix is tracked at hyperium/h2#812. The fix was included in h2 0.4.8. The 2.2.x stream already picks up this fix. The 2.1.x stream (pinned to source tags v0.3.8 and v0.3.12) does not include this fix.
