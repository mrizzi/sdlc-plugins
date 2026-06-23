# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-55123 (tokio < 1.42.0)

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES | |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES | |

All supported versions across both streams ship tokio < 1.42.0 and are affected.

## Cross-Stream Analysis

This issue is scoped to stream **rhtpa-2.2** (from summary suffix `[rhtpa-2.2]`).
However, version impact analysis reveals that stream **rhtpa-2.1** is also affected:

- Stream rhtpa-2.1 ships tokio 1.40.0 (threshold: 1.42.0) -- **AFFECTED**
- Stream rhtpa-2.2 ships tokio 1.41.1 (threshold: 1.42.0) -- **AFFECTED**

### Stream-Scoped Impact (for this issue TC-8020)

Since TC-8020 is scoped to rhtpa-2.2, only rhtpa-2.2 versions are in scope for Affects Versions correction and Case A remediation:

| Version | tokio version | Affected? | In Scope? |
|---------|---------------|-----------|-----------|
| RHTPA 2.1.0 | 1.40.0 | YES | No (rhtpa-2.1 stream) |
| RHTPA 2.1.1 | 1.40.0 | YES | No (rhtpa-2.1 stream) |
| RHTPA 2.2.0 | 1.41.1 | YES | **Yes** (rhtpa-2.2 stream) |
| RHTPA 2.2.1 | 1.41.1 | YES | **Yes** (rhtpa-2.2 stream) |

## Dependency Chain Context (Step 2.3.5)

Dependency chain for tokio:
  backend (workspace) -> tokio (direct runtime dependency)
  Profile: production (tokio is the async runtime)

tokio is a direct dependency of the rhtpa-backend workspace and is present in all versions across both streams.

## Affects Versions Correction (Step 3)

PSIRT-assigned Affects Versions: `[RHTPA 2.2.0, RHTPA 2.2.1]`
Proposed Affects Versions (scoped to rhtpa-2.2): `[RHTPA 2.2.0, RHTPA 2.2.1]`

**Affects Versions are already correct** -- PSIRT correctly assigned the two rhtpa-2.2 versions. No correction needed.

## Sibling CVE Jira Search (Step 4)

JQL: `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020`

**No sibling Vulnerability issues found** for CVE-2026-55123 in any stream, including rhtpa-2.1.

This means stream rhtpa-2.1 has no CVE Jira tracking this vulnerability -- triggering Case B (cross-stream preemptive remediation).
