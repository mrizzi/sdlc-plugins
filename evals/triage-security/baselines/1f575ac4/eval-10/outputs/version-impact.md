# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-55123 (tokio < 1.42.0)

### Current stream (rhtpa-2.2) -- in scope for TC-8020

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES | v0.4.5 |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES | v0.4.8 |

### Cross-stream analysis (rhtpa-2.1) -- outside TC-8020 scope

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES | v0.3.8 |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES | v0.3.12 |

### Summary

- **Fix threshold**: tokio >= 1.42.0 (from Jira description, cross-validated with external CVE data)
- **Current stream (rhtpa-2.2)**: ALL versions affected (tokio 1.41.1 < 1.42.0)
- **Other stream (rhtpa-2.1)**: ALL versions affected (tokio 1.40.0 < 1.42.0)

### Cross-stream impact

Stream rhtpa-2.1 ships tokio 1.40.0 which is below the fix threshold of 1.42.0. This stream is also affected by CVE-2026-55123.

A JQL search for sibling CVE Jiras with label CVE-2026-55123 returns **no results** for stream rhtpa-2.1 -- no CVE Jira exists for that stream. This triggers Step 7 Case B (preemptive remediation).

### Dependency Chain Context

```
Dependency chain for tokio:
  backend (workspace) -> tokio (direct dependency)
  Profile: production (tokio is a core async runtime dependency)
  Present in all versions across both streams.
```

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | Upstream fix available (PR #7001) |
| 2.1.x | Cargo | release/0.3.z | Upstream fix available (PR #7001) |
