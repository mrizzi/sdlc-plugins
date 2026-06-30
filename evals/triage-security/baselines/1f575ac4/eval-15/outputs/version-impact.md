# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

### Scoped stream: 2.2.x

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | ships fixed version |

### Cross-stream analysis: 2.1.x

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | |

## Dependency Chain Context

```
Dependency chain for quinn-proto (Cargo):
  Ecosystem: Cargo (source dependency)
  Lock file: Cargo.lock
  SBOM verification: not applicable (source dependency ecosystem -- Cargo.lock is the source of truth)

  quinn-proto is a QUIC transport protocol implementation crate.
  Present in all versions across both streams (2.1.x and 2.2.x).
  Fixed in version 0.11.14 (first shipped in 2.2.3 / build v0.4.11).
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 | NO |

## Summary

- **2.2.x stream** (scoped): versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fix (quinn-proto 0.11.14).
- **2.1.x stream** (cross-stream): all versions (2.1.0, 2.1.1) are affected. The upstream branch `release/0.3.z` has NOT been fixed yet.
- The upstream fix is available on `release/0.4.z` (2.2.x stream) but not on `release/0.3.z` (2.1.x stream).
