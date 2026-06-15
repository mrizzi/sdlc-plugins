# Step 2: Version Impact Analysis

## Vulnerability Parameters

- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Affected range**: < 0.11.14
- **Fixed version**: 0.11.14
- **Ecosystem**: Cargo (lock file: `Cargo.lock`)

## Version Impact Table

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Pinned Tag | quinn-proto Version | Affected (< 0.11.14)? | Notes |
|---------|-------|------------|---------------------|------------------------|-------|
| 2.1.0 | 0.3.8 | `v0.3.8` | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | 0.3.12 | `v0.3.12` | 0.11.9 | YES | 0.11.9 < 0.11.14 |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Pinned Tag | quinn-proto Version | Affected (< 0.11.14)? | Notes |
|---------|-------|------------|---------------------|------------------------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | 0.4.8 | `v0.4.8` | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | 0.4.9 | `v0.4.8` | 0.11.12 | YES | Retag of v0.4.8; carry forward from 2.2.1 |
| 2.2.3 | 0.4.11 | `v0.4.11` | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | 0.4.12 | `v0.4.12` | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

## Summary

- **Total versions assessed**: 7 (2 in 2.1.x stream, 5 in 2.2.x stream)
- **Affected versions**: 2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2
- **Not affected versions**: 2.2.3, 2.2.4
- **Fix introduced at**: v0.4.11 (build 0.4.11, version 2.2.3) where quinn-proto was bumped to 0.11.14
