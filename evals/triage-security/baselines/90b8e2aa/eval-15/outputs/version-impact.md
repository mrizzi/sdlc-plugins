# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Dependency Chain Context

```
Dependency chain for quinn-proto (Cargo):
  Ecosystem: Cargo (Rust crate)
  Lock file: Cargo.lock
  Profile: production (runtime dependency)
```

## Stream Impact Summary

- **2.2.x stream** (issue scope): versions 2.2.0, 2.2.1, 2.2.2 are affected; versions 2.2.3, 2.2.4 are NOT affected (ship quinn-proto 0.11.14, which is the fix version).
- **2.1.x stream** (cross-stream): versions 2.1.0, 2.1.1 are affected (ship quinn-proto 0.11.9). This stream is outside the issue's scope but is impacted -- triggers Case B (cross-stream impact).

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (at v0.4.11+) | YES |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (at v0.3.12) | NO |

The upstream fix is available on the `release/0.4.z` branch (2.2.x stream) but NOT on the `release/0.3.z` branch (2.1.x stream).
