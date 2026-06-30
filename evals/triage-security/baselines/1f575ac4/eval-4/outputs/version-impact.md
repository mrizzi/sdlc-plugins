# Version Impact Analysis — TC-8004

## CVE-2026-33501 (h2 < 0.4.8)

Fix threshold: h2 >= 0.4.8

### Version Impact Table

| Version | Stream | Build Tag | h2 Version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | **YES** | < 0.4.8 — vulnerable |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | **YES** | < 0.4.8 — vulnerable |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | >= 0.4.8 — fixed |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | >= 0.4.8 — fixed |
| 2.2.2 | 2.2.x | v0.4.9 | — | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | >= 0.4.8 — fixed |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | >= 0.4.8 — fixed |

### Stream Impact Summary

| Stream | Affected Versions | Not Affected Versions | Impact |
|--------|-------------------|-----------------------|--------|
| 2.1.x | 2.1.0, 2.1.1 | — | **ALL versions affected** |
| 2.2.x | — | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | **No versions affected** |

### Analysis

The version impact is **mixed across streams**:

- **2.1.x stream**: All versions (2.1.0 and 2.1.1) ship h2 0.4.5, which is below the fix threshold of 0.4.8. Both versions are **affected**.
- **2.2.x stream**: All versions ship h2 >= 0.4.8. Version 2.2.0 ships exactly h2 0.4.8 (the fix version), and later versions ship h2 0.4.9. No versions in this stream are affected.

### Dependency Chain

```
Dependency chain for h2 (Cargo):
  backend (workspace) -> hyper -> h2
  Ecosystem: Cargo (Rust crate)
  Lock file: Cargo.lock
  Profile: production (h2 is a runtime HTTP/2 dependency via hyper)

  2.1.x stream: h2 0.4.5 present in v0.3.8 and v0.3.12
  2.2.x stream: h2 0.4.8+ present from v0.4.5 onward (fixed at stream inception)
```

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Status |
|--------|-----------|-----------------|------------|
| 2.1.x | Cargo | release/0.3.z | Needs upstream backport — h2 must be bumped to >= 0.4.8 |
| 2.2.x | Cargo | release/0.4.z | Already fixed — ships h2 >= 0.4.8 |

The upstream fix PR is [hyperium/h2#812](https://github.com/hyperium/h2/pull/812). The 2.1.x stream requires a backport to bump h2 from 0.4.5 to >= 0.4.8 on the `release/0.3.z` branch.
