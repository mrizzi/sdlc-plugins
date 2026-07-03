# Version Impact Analysis — CVE-2026-33501

## Version Impact Table

Version Impact for CVE-2026-33501 (h2 < 0.4.8):

| Stream | Version | Build Tag | h2 version | Affected? | Notes |
|--------|---------|-----------|------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.4.5 | **YES** | < 0.4.8 |
| 2.1.x | 2.1.1 | v0.3.12 | 0.4.5 | **YES** | < 0.4.8 |
| 2.2.x | 2.2.0 | v0.4.5 | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.x | 2.2.1 | v0.4.8 | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.x | 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.4.9 | NO | >= 0.4.8 (fixed) |
| 2.2.x | 2.2.4 | v0.4.12 | 0.4.9 | NO | >= 0.4.8 (fixed) |

## Stream Impact Summary

| Stream | Affected? | Affected Versions | Details |
|--------|-----------|-------------------|---------|
| 2.1.x | **YES** | 2.1.0, 2.1.1 | All versions ship h2 0.4.5 (vulnerable) |
| 2.2.x | NO | (none) | All versions ship h2 >= 0.4.8 (fixed) |

## Mixed Impact Analysis

This CVE exhibits **mixed impact across streams**:

- **2.1.x stream**: ALL versions are affected. Both 2.1.0 (build v0.3.8) and 2.1.1 (build v0.3.12) ship h2 0.4.5, which is within the vulnerable range (< 0.4.8). Remediation is required for this stream.
- **2.2.x stream**: NO versions are affected. The earliest version (2.2.0, build v0.4.5) already ships h2 0.4.8 (the fix version). All subsequent versions (2.2.1 through 2.2.4) ship h2 0.4.8 or 0.4.9, all of which are at or above the fix threshold.

## Dependency Chain Context

```
Dependency chain for h2 (Cargo):
  backend (workspace) -> hyper -> h2
  Ecosystem: Cargo (Cargo.lock)
  Lock file: Cargo.lock
  Source repository: backend

  2.1.x stream: h2 0.4.5 present in both v0.3.8 and v0.3.12
  2.2.x stream: h2 0.4.8+ present from v0.4.5 onward (fix already applied)
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | Needs backport -- h2 must be bumped to >= 0.4.8 |
| 2.2.x | Cargo | release/0.4.z | Already fixed -- ships h2 >= 0.4.8 |
