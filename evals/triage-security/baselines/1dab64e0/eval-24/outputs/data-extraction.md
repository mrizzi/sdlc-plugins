# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |
| Ecosystem | Cargo (Rust crate) |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)
- Issue is **scoped** to stream 2.2.x only

## Deployment Context

Source Repositories table does not have a Deployment Context column. Per backward compatibility rules, all repositories default to `upstream`. Coordination guidance is omitted from remediation task descriptions.

## Version Impact Analysis

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | quinn-proto | Affected? | Notes |
|--------|---------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | 0.11.14 | NO | at or above fix threshold |
| 2.2.x | 2.2.4 | 0.11.14 | NO | at or above fix threshold |

### Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: source dependency (Cargo crate)
  Ecosystem: Cargo
  Lock file: Cargo.lock
  Check command: git show <tag>:Cargo.lock
```

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.1.x | Cargo | release/0.3.z | Upstream branch configured for backport |
| 2.2.x | Cargo | release/0.4.z | Upstream branch configured for backport |

## Affects Versions Correction

- **Current (PSIRT-assigned):** RHTPA 2.0.0
- **Proposed (scoped to 2.2.x):** RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Rationale:** RHTPA 2.0.0 does not correspond to any version in the supportability matrix. Lock file analysis at pinned commits shows versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto < 0.11.14 (vulnerable). Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (fixed). Correction is scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`.

## Cross-Stream Impact (Case B)

Stream 2.1.x is also affected (all versions ship quinn-proto 0.11.9, which is below the fix threshold of 0.11.14). Since the issue is scoped to 2.2.x, the 2.1.x impact is handled via Case B cross-stream proactive remediation.
