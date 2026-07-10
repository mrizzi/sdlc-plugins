# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-33501 (h2 < 0.4.8)

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 |
| 2.2.2 | 2.2.x | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

## Summary by Stream

| Stream | Affected? | Details |
|--------|-----------|---------|
| 2.1.x | **YES** | All versions (2.1.0, 2.1.1) ship h2 0.4.5, which is below the fix threshold of 0.4.8 |
| 2.2.x | **NO** | All versions ship h2 >= 0.4.8, which is at or above the fix threshold |

This is a **mixed impact** scenario: the 2.1.x stream is fully affected while the 2.2.x stream already ships the patched version.

## Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: direct or transitive Cargo dependency (lock file confirms presence)
  Ecosystem: Cargo
  Profile: production (h2 is a runtime HTTP/2 protocol dependency)

  Stream 2.1.x: h2 0.4.5 -- VULNERABLE
  Stream 2.2.x: h2 0.4.8+ -- FIXED
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Status | Notes |
|--------|-----------|-----------------|------------|-------|
| 2.1.x | Cargo | release/0.3.z | Needs fix | h2 must be bumped from 0.4.5 to >= 0.4.8 |
| 2.2.x | Cargo | release/0.4.z | Already fixed | h2 is already >= 0.4.8 in all versions |

Upstream fix PR: [hyperium/h2#812](https://github.com/hyperium/h2/pull/812)

The fix is available upstream (h2 0.4.8 was released). Remediation for the 2.1.x stream requires bumping the h2 dependency in the backend source repo on the `release/0.3.z` branch, then propagating the updated source reference in the rhtpa-release.0.3.z Konflux release repo.
