# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-55123 (tokio < 1.42.0)

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES | Cross-stream (outside issue scope) |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES | Cross-stream (outside issue scope) |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES | Within issue scope |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES | Within issue scope |

Fix threshold: 1.42.0 (from Jira description; confirmed by cross-stream analysis)

## Cross-Stream Impact Summary

- **rhtpa-2.2** (issue scope): RHTPA 2.2.0 and 2.2.1 are affected (tokio 1.41.1 < 1.42.0)
- **rhtpa-2.1** (outside issue scope): RHTPA 2.1.0 and 2.1.1 are affected (tokio 1.40.0 < 1.42.0)

Stream rhtpa-2.1 is also affected but is outside the scope of TC-8020 (which is scoped to rhtpa-2.2). This triggers Case B (cross-stream proactive remediation).

## Ecosystem Mappings

### Stream rhtpa-2.1 (2.1.x)

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |

### Stream rhtpa-2.2 (2.2.x)

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Library | Fix Threshold | Status |
|--------|-----------|-----------------|---------|---------------|--------|
| rhtpa-2.2 | Cargo | release/0.4.z | tokio | 1.42.0 | Needs upstream fix |
| rhtpa-2.1 | Cargo | release/0.3.z | tokio | 1.42.0 | Needs upstream fix |

## Sibling CVE Jira Search (Step 4)

JQL: `project = TC AND issuetype = 10024 AND labels = CVE-2026-55123 AND summary ~ "rhtpa-2.1"`

**Result**: No sibling Vulnerability issues found for CVE-2026-55123 in stream rhtpa-2.1.

This means stream rhtpa-2.1 has no CVE Jira and requires preemptive remediation tasks (Case B).
