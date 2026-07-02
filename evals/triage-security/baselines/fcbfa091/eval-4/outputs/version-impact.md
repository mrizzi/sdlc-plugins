# Version Impact — TC-8004

## Version Impact for CVE-2026-33501 (h2 < 0.4.8)

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | YES | < 0.4.8 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | YES | < 0.4.8 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | >= 0.4.8 (fixed version) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | >= 0.4.8 (fixed version) |
| 2.2.2 | 2.2.x | v0.4.9 | 0.4.8 | NO | retag of 2.2.1 |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | >= 0.4.8 |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | >= 0.4.8 |

## Stream Impact Summary

| Stream | Affected? | Affected Versions | Shipped h2 |
|--------|-----------|-------------------|------------|
| 2.1.x | YES | 2.1.0, 2.1.1 | 0.4.5 (vulnerable) |
| 2.2.x | NO | None | 0.4.8+ (fixed) |

All versions in the 2.1.x stream ship h2 0.4.5, which is within the affected range (< 0.4.8). All versions in the 2.2.x stream ship h2 0.4.8 or later, which includes the fix. The 2.2.x stream was never affected.

## Dependency Chain

```
Dependency chain for h2 (Cargo):
  backend (workspace) -> hyper -> h2
  Lock file: Cargo.lock
  Profile: production (h2 is a runtime dependency via hyper)

  2.1.x stream: h2 0.4.5 shipped in all versions (v0.3.8, v0.3.12)
  2.2.x stream: h2 0.4.8+ shipped in all versions (v0.4.5 onward) — already fixed
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.1.x | Cargo | release/0.3.z | Fix needed — h2 must be bumped to >= 0.4.8 |
| 2.2.x | Cargo | release/0.4.z | Already ships h2 >= 0.4.8 — no action needed |
