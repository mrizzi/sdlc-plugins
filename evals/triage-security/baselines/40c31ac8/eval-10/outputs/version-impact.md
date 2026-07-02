# Step 2 -- Version Impact Analysis for TC-8020 (CVE-2026-55123)

## Version Impact Table

Version Impact for CVE-2026-55123 (tokio < 1.42.0):

| Version | Stream | tokio version | Fix Threshold | Affected? | Notes |
|---------|--------|---------------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | 1.42.0 | YES | pinned at v0.3.8 |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | 1.42.0 | YES | pinned at v0.3.12 |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | 1.42.0 | YES | pinned at v0.4.5 |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | 1.42.0 | YES | pinned at v0.4.8 |
| RHTPA 2.2.2 | rhtpa-2.2 | -- | 1.42.0 | YES | retag of 2.2.1 (same as v0.4.8) |

All versions across both streams ship tokio < 1.42.0 and are affected.

## Cross-Stream Impact Summary

- **Stream rhtpa-2.2** (issue scope): RHTPA 2.2.0 and 2.2.1 are affected (tokio 1.41.1), plus 2.2.2 (retag of 2.2.1)
- **Stream rhtpa-2.1** (outside issue scope): RHTPA 2.1.0 and 2.1.1 are affected (tokio 1.40.0)

This triggers **Case A** (remediation for the current stream) and **Case B** (cross-stream proactive remediation for rhtpa-2.1).

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for tokio:
  backend (workspace) -> tokio (runtime dependency)
  Profile: production (tokio is a core runtime dependency)
  Ecosystem: Cargo
```

tokio is a fundamental async runtime crate for Rust -- it is a direct dependency of the backend workspace.

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Upstream Fix PR | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | tokio-rs/tokio#7001 | Needs verification |
| 2.2.x | Cargo | release/0.4.z | tokio-rs/tokio#7001 | Needs verification |

The upstream fix PR (https://github.com/tokio-rs/tokio/pull/7001) targets the tokio crate itself. Remediation requires bumping the tokio dependency in the rhtpa-backend Cargo.lock to >= 1.42.0 on each stream's release branch.
