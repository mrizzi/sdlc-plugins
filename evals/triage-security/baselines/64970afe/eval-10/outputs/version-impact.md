# Version Impact Analysis — CVE-2026-55123 (tokio)

## Version Impact Table

Version impact for CVE-2026-55123 (tokio < 1.42.0, fixed in 1.42.0):

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES | |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES | |

All supported versions across both streams ship tokio < 1.42.0 and are affected.

## Cross-Stream Impact Summary

- **Issue scope**: rhtpa-2.2 (stream 2.2.x)
- **In-scope versions affected**: RHTPA 2.2.0 (tokio 1.41.1), RHTPA 2.2.1 (tokio 1.41.1)
- **Out-of-scope versions affected**: RHTPA 2.1.0 (tokio 1.40.0), RHTPA 2.1.1 (tokio 1.40.0)
- **Fix threshold**: tokio >= 1.42.0

Stream rhtpa-2.1 is also affected. tokio 1.40.0 is shipped in both RHTPA 2.1.0 and RHTPA 2.1.1, which is below the fix threshold of 1.42.0.

## Dependency Chain Context

```
Dependency chain for tokio:
  backend (workspace) -> tokio
  Type: direct dependency
  Profile: production (tokio is a runtime dependency)
  
Remediation: bump tokio to >= 1.42.0 in Cargo.toml
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fixed? | Notes |
|--------|-----------|-----------------|--------|-------|
| 2.2.x | Cargo | release/0.4.z | To be verified | Upstream fix PR: tokio-rs/tokio#7001 |
| 2.1.x | Cargo | release/0.3.z | To be verified | Upstream fix PR: tokio-rs/tokio#7001 |
