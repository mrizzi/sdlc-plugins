# Step 2 -- Version Impact Analysis

## Vulnerability Details

- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Affected range**: versions before 0.11.14 (< 0.11.14)
- **Fixed version**: 0.11.14

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.1.0 | `v0.3.8` | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | `v0.3.12` | 0.11.9 | YES | 0.11.9 < 0.11.14 |

### Stream 2.2.x (rhtpa-release.0.4.z) -- Issue-scoped stream

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | `v0.4.8` | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | `v0.4.9` | -- | YES | retag of 2.2.1 (same as 2.2.1; v0.4.9 = retag of v0.4.8, carries forward 0.11.12) |
| 2.2.3 | `v0.4.11` | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed version) |
| 2.2.4 | `v0.4.12` | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed version) |

### Combined Impact Summary

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | fixed version |

## Dependency Chain Context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) -> quinn-proto (via QUIC transport dependency chain)
  Ecosystem: Cargo (Cargo.lock)
  Lock file: Cargo.lock
  Check command: git show <tag>:Cargo.lock

  Affected versions: 2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2
  First fixed version in product: 2.2.3 (tag v0.4.11, quinn-proto 0.11.14)
  Not fixed in: 2.1.x stream (all versions ship 0.11.9)
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.1.x | Cargo | `release/0.3.z` | Needs upstream check at branch HEAD |
| 2.2.x | Cargo | `release/0.4.z` | Fix already present in 2.2.3+ (v0.4.11 ships 0.11.14) |

The fix was introduced in the 2.2.x stream starting at version 2.2.3 (build 0.4.11). Versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream are affected. All versions in the 2.1.x stream are affected.
