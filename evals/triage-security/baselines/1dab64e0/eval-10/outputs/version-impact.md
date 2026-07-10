# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-55123 (tokio < 1.42.0)

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES | |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES | |

Fix threshold: 1.42.0 (from Jira description and CVE record)

## Cross-Stream Summary

- **Stream rhtpa-2.2** (issue scope): ALL versions affected (tokio 1.41.1 < 1.42.0)
- **Stream rhtpa-2.1** (outside issue scope): ALL versions affected (tokio 1.40.0 < 1.42.0)

## Dependency Chain Context

```
Dependency chain for tokio:
  backend (workspace) -> tokio
  Type: direct dependency (Cargo)
  Profile: production (tokio is a runtime dependency)
  Ecosystem: Cargo
  Lock file: Cargo.lock
  Check command: git show <tag>:Cargo.lock

Remediation: bump tokio to >= 1.42.0 in Cargo.toml
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Upstream Fix PR | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| rhtpa-2.2 | Cargo | release/0.4.z | tokio-rs/tokio#7001 | Upstream fix available |
| rhtpa-2.1 | Cargo | release/0.3.z | tokio-rs/tokio#7001 | Upstream fix available |

## Sibling CVE Jira Search (Step 4)

JQL: `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020`

Results for stream rhtpa-2.1: **No sibling Vulnerability issues found.**

No CVE Jira exists for stream rhtpa-2.1 -- this triggers Case B (preemptive remediation).
