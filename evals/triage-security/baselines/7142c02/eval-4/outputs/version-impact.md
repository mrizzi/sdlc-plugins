# Step 2 -- Version Impact Analysis: CVE-2026-33501

## Version Impact Table

Version Impact for CVE-2026-33501 (h2 < 0.4.8):

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | YES | h2 0.4.5 < 0.4.8 (fix threshold) |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | YES | h2 0.4.5 < 0.4.8 (fix threshold) |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | h2 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | h2 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.2 | 2.2.x | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 (above fix threshold) |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 (above fix threshold) |

## Stream Impact Summary

| Stream | Affected? | Versions Affected | h2 Version Shipped |
|--------|-----------|-------------------|--------------------|
| 2.1.x | YES | 2.1.0, 2.1.1 | 0.4.5 (vulnerable) |
| 2.2.x | NO | None | 0.4.8+ (fixed) |

## Dependency Chain Context

```
Dependency chain for h2 (Cargo):
  backend (workspace) -> hyper -> h2
  Ecosystem: Cargo
  Lock file: Cargo.lock
  Profile: production (h2 is a runtime dependency via hyper HTTP/2 support)

  2.1.x stream: h2 0.4.5 (vulnerable, < 0.4.8)
  2.2.x stream: h2 0.4.8+ (fixed, >= 0.4.8)
```

The h2 crate is a transitive dependency pulled in via hyper for HTTP/2 protocol support. It is present in all versions across both streams but only the 2.1.x stream ships a vulnerable version.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | h2 at Branch HEAD | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.1.x | Cargo | release/0.3.z | Needs verification | Unknown -- requires git show |
| 2.2.x | Cargo | release/0.4.z | >= 0.4.8 | YES (already shipping fixed version) |

The 2.2.x stream already ships h2 0.4.8+ in all released versions, confirming the fix was picked up starting with the v0.4.5 build tag (version 2.2.0).

For the 2.1.x stream, the upstream branch `release/0.3.z` would need to be checked to determine if the fix has been backported. Based on the lock file data, the latest 2.1.x release (2.1.1, tag v0.3.12) still ships h2 0.4.5, indicating the fix has not yet been incorporated into this stream.
