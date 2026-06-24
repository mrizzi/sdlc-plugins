# Step 2 -- Version Impact Analysis: TC-8020

## CVE-2026-55123 (tokio < 1.42.0)

Fix threshold: **1.42.0** (from Jira description, cross-validated with external CVE data)

### Version Impact Table

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES | |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES | |

All supported versions across both streams ship tokio < 1.42.0 and are affected.

### Cross-Stream Impact Summary

- **Stream rhtpa-2.2** (issue scope): RHTPA 2.2.0 and 2.2.1 are affected (tokio 1.41.1 < 1.42.0)
- **Stream rhtpa-2.1** (outside issue scope): RHTPA 2.1.0 and 2.1.1 are also affected (tokio 1.40.0 < 1.42.0)

### Dependency Chain Context

```
Dependency chain for tokio:
  backend (workspace) -> tokio (direct runtime dependency)
  Ecosystem: Cargo
  Profile: production (tokio is a core async runtime dependency)

  Stream rhtpa-2.1: tokio 1.40.0 (all versions)
  Stream rhtpa-2.2: tokio 1.41.1 (all versions)
```

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Threshold | Notes |
|--------|-----------|-----------------|---------------|-------|
| 2.1.x | Cargo | release/0.3.z | 1.42.0 | Requires upstream backport |
| 2.2.x | Cargo | release/0.4.z | 1.42.0 | Requires upstream backport |

### Source Pinning Method

- **backend**: `artifacts.lock.yaml` (download URL contains tag)
- Stream 2.1.x tags: v0.3.8 (2.1.0), v0.3.12 (2.1.1)
- Stream 2.2.x tags: v0.4.5 (2.2.0), v0.4.8 (2.2.1)
