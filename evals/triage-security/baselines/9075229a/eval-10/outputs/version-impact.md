# Step 2 -- Version Impact Analysis: CVE-2026-55123

## Fix Threshold

- Library: tokio
- Affected range: versions before 1.42.0
- Fix threshold: **1.42.0** (from Jira description, cross-validated with external CVE data)

## Version Impact Table

Version Impact for CVE-2026-55123 (tokio < 1.42.0):

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | 2.1.x (rhtpa-2.1) | 1.40.0 | YES | Source tag: v0.3.8 |
| RHTPA 2.1.1 | 2.1.x (rhtpa-2.1) | 1.40.0 | YES | Source tag: v0.3.12 |
| RHTPA 2.2.0 | 2.2.x (rhtpa-2.2) | 1.41.1 | YES | Source tag: v0.4.5 |
| RHTPA 2.2.1 | 2.2.x (rhtpa-2.2) | 1.41.1 | YES | Source tag: v0.4.8 |
| RHTPA 2.2.2 | 2.2.x (rhtpa-2.2) | 1.41.1 | YES | retag of 2.2.1 (same source: v0.4.8) |

## Cross-Stream Impact Summary

| Stream | Versions Affected | tokio version | Within issue scope? |
|--------|-------------------|---------------|---------------------|
| 2.2.x (rhtpa-2.2) | 2.2.0, 2.2.1, 2.2.2 | 1.41.1 | YES (issue scoped to [rhtpa-2.2]) |
| 2.1.x (rhtpa-2.1) | 2.1.0, 2.1.1 | 1.40.0 | NO (cross-stream impact) |

**Cross-stream finding**: Stream rhtpa-2.1 is also affected (tokio 1.40.0 < fix threshold 1.42.0).
This stream is outside the current issue's scope and requires Case B handling.

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for tokio:
  backend (workspace) -> tokio (direct runtime dependency)
  Profile: production (tokio is a core async runtime dependency)
  Ecosystem: Cargo
```

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Repository | Upstream Branch | Fix Status |
|--------|-----------|------------|-----------------|------------|
| 2.2.x | Cargo | backend | release/0.4.z | Upstream fix PR: tokio-rs/tokio#7001 |
| 2.1.x | Cargo | backend | release/0.3.z | Upstream fix PR: tokio-rs/tokio#7001 |
