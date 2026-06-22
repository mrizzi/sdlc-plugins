# Version Impact Analysis — TC-8004

## CVE-2026-33501: h2 (versions before 0.4.8)

### Version Impact Table

| Version | Stream | Build Tag | h2 Version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.4.8 | NO | 0.4.8 >= 0.4.8 (fixed) |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.4.8 | NO | 0.4.8 >= 0.4.8 (fixed) |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.4.9 | NO | 0.4.9 >= 0.4.8 (fixed) |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.4.9 | NO | 0.4.9 >= 0.4.8 (fixed) |

### Stream Impact Summary

| Stream | Affected Versions | Not Affected Versions | Impact |
|--------|-------------------|-----------------------|--------|
| 2.1.x | 2.1.0, 2.1.1 | -- | **ALL versions affected** |
| 2.2.x | -- | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | **No versions affected** |

### Mixed Impact Analysis

This is a **mixed impact** scenario across streams:

- **2.1.x stream**: ALL versions ship h2 0.4.5, which is within the vulnerable range (< 0.4.8). Both 2.1.0 and 2.1.1 are **affected**.
- **2.2.x stream**: ALL versions ship h2 >= 0.4.8 (the fixed version). The earliest 2.2.x version (2.2.0, build tag v0.4.5) already includes h2 0.4.8. No 2.2.x versions are affected.

### Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> hyper -> h2
  Ecosystem: Cargo (source dependency)
  Lock file: Cargo.lock

  2.1.x stream: h2 0.4.5 present in all versions (v0.3.8, v0.3.12)
  2.2.x stream: h2 0.4.8+ present in all versions (v0.4.5 onward)
  
  The 2.2.x stream picked up the h2 fix at the stream's inception --
  the first 2.2.x build (v0.4.5, shipping with 2.2.0) already includes h2 0.4.8.
```

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fixed in h2 | Status |
|--------|-----------|-----------------|-------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | 0.4.8 | Needs upstream backport -- h2 must be bumped from 0.4.5 to >= 0.4.8 |
| 2.2.x | Cargo | `release/0.4.z` | 0.4.8+ | Already fixed -- all versions ship h2 >= 0.4.8 |
