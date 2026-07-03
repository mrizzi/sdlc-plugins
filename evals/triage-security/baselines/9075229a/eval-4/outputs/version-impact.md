# Version Impact Analysis — TC-8004

## CVE-2026-33501 (h2 < 0.4.8)

Version Impact for CVE-2026-33501 (h2 versions before 0.4.8):

| Version | Stream | Source Tag | h2 Version | Affected? | Notes |
|---------|--------|------------|------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.4.5 | **YES** | < 0.4.8 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.4.5 | **YES** | < 0.4.8 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.4.8 | NO | = 0.4.8 (fixed) |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.4.8 | NO | = 0.4.8 (fixed) |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.4.9 | NO | > 0.4.8 (fixed) |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.4.9 | NO | > 0.4.8 (fixed) |

## Impact Summary

- **Stream 2.1.x**: AFFECTED -- all versions (2.1.0, 2.1.1) ship h2 0.4.5, which is below the fix threshold of 0.4.8.
- **Stream 2.2.x**: NOT AFFECTED -- all versions ship h2 >= 0.4.8. Version 2.2.0 already ships the fix version (0.4.8), and later versions ship 0.4.9.

This is a **mixed impact** scenario: the vulnerability affects the 2.1.x stream but does not affect the 2.2.x stream.

## Dependency Chain Context

```
Dependency chain for h2 (Cargo):
  backend (workspace) -> hyper -> h2
  Profile: production (hyper is a runtime HTTP dependency)

  2.1.x stream: h2 0.4.5 (affected — below fix threshold 0.4.8)
  2.2.x stream: h2 0.4.8+ (not affected — at or above fix threshold)
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.1.x | Cargo | `release/0.3.z` | Affected — h2 must be bumped to >= 0.4.8 |
| 2.2.x | Cargo | `release/0.4.z` | Not affected — already ships h2 >= 0.4.8 |
