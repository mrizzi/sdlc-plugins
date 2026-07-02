# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | Backend Tag | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | ships fixed version |

**Fix threshold**: quinn-proto >= 0.11.14

Versions 2.1.0, 2.1.1, 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto versions
below the 0.11.14 fix threshold and are vulnerable. Versions 2.2.3 and 2.2.4
ship quinn-proto 0.11.14 (the fixed version) and are not affected.

## Dependency Chain Context

```
Dependency chain for quinn-proto (Cargo):
  Ecosystem: Cargo (Rust crate)
  Lock file: Cargo.lock
  Repository: backend

  quinn-proto is a QUIC protocol implementation crate. It provides the
  protocol state machine used by the quinn crate for QUIC transport.

  Affected range: versions before 0.11.14
  Fixed in: 0.11.14
  Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
```

## Upstream Fix Status

The upstream fix check uses the Upstream Branch column from the Ecosystem
Mappings table for each stream.

| Stream | Ecosystem | Upstream Branch | Backend Tag at HEAD | quinn-proto at HEAD | Fixed? |
|--------|-----------|-----------------|---------------------|---------------------|--------|
| 2.1.x | Cargo | release/0.3.z | -- | -- | Unknown (would require git show on branch HEAD) |
| 2.2.x | Cargo | release/0.4.z | -- | -- | Unknown (would require git show on branch HEAD) |

Note: The latest released versions in the 2.2.x stream (2.2.3 at v0.4.11
and 2.2.4 at v0.4.12) already ship quinn-proto 0.11.14, indicating the
upstream fix has been incorporated into the release/0.4.z branch. The 2.1.x
stream's latest release (2.1.1 at v0.3.12) still ships quinn-proto 0.11.9,
indicating the fix has not yet been backported to release/0.3.z.
