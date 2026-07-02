# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-33501 (h2 < 0.4.8)

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | **YES** | ships vulnerable h2 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | **YES** | ships vulnerable h2 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | ships fixed version (0.4.8) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | ships fixed version (0.4.8) |
| 2.2.2 | 2.2.x | v0.4.9 | _(retag)_ | NO | same as 2.2.1 (retag of v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | ships version above fix threshold |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | ships version above fix threshold |

## Impact Summary

- **2.1.x stream**: **AFFECTED** -- all versions (2.1.0, 2.1.1) ship h2 0.4.5, which is below the fix threshold of 0.4.8.
- **2.2.x stream**: **NOT AFFECTED** -- all versions ship h2 >= 0.4.8 (the fixed version). The earliest 2.2.x release (2.2.0) already includes the patched h2 0.4.8.

This is a mixed-impact scenario: the vulnerability only affects the older 2.1.x stream while the newer 2.2.x stream ships the patched dependency.

## Dependency Chain Context

```
Dependency chain for h2 (Cargo):
  backend (workspace) -> hyper -> h2
  Ecosystem: Cargo (Cargo.lock)
  Profile: production (h2 is a runtime HTTP/2 dependency via hyper)

  2.1.x stream: h2 0.4.5 (vulnerable) -- present in all 2.1.x versions
  2.2.x stream: h2 0.4.8+ (fixed) -- patched from the earliest 2.2.x release
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | h2 version at latest tag | Fixed? |
|--------|-----------|-----------------|--------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.4.5 (at v0.3.12) | **NO** -- upstream branch still ships vulnerable version |
| 2.2.x | Cargo | release/0.4.z | 0.4.9 (at v0.4.12) | YES -- already ships fixed version |
