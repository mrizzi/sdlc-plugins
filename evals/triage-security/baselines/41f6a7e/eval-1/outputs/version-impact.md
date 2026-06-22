# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | YES | retag of 2.2.1 (same as v0.4.8, quinn-proto 0.11.12) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | ships fixed version |

### Dependency Chain Context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) -> [transitive via QUIC stack] -> quinn-proto
  Ecosystem: Cargo (source dependency in Cargo.lock)

  Present in: all versions across both streams (2.1.x and 2.2.x)
  Fixed starting from: 2.2.3 (build 0.4.11, tag v0.4.11) which ships quinn-proto 0.11.14
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD (tag) | Fixed? |
|--------|-----------|-----------------|----------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.12) | YES |

### Analysis

- **Stream 2.1.x**: All versions (2.1.0, 2.1.1) ship quinn-proto 0.11.9, which is vulnerable (< 0.11.14). The upstream branch `release/0.3.z` at its latest tag (v0.3.12) still has 0.11.9 -- NOT fixed upstream.
- **Stream 2.2.x**: Versions 2.2.0 through 2.2.2 are affected. Version 2.2.3 onward ships the fixed version 0.11.14. The upstream branch `release/0.4.z` at its latest tag (v0.4.12) has 0.11.14 -- already fixed upstream.
- The fix was introduced in build 0.4.11 (version 2.2.3, released 2026-03-23).
