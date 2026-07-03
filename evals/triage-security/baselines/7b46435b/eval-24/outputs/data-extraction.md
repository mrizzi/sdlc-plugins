# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo `rhtpa-release.0.4.z`). This issue is **scoped to the 2.2.x stream** -- Steps 3 and 4 apply only to 2.2.x versions.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Based on the Ecosystem Mappings table in the security matrix, the applicable ecosystem is **Cargo**.

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Source repository: backend
- Upstream branch (2.1.x): `release/0.3.z`
- Upstream branch (2.2.x): `release/0.4.z`

## Deployment Context

The Source Repositories table in CLAUDE.md does not have a Deployment Context column. Per backward compatibility rules, all repositories default to `upstream`. However, since the column is absent, coordination guidance is omitted from remediation task descriptions.

## Version Impact Analysis

### Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Build Tag | quinn-proto | Affected? | Notes |
|--------|---------|-----------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | `v0.3.8` | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | `v0.3.12` | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | `v0.4.5` | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | `v0.4.8` | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | `v0.4.9` | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | `v0.4.11` | 0.11.14 | NO | ships fixed version |
| 2.2.x | 2.2.4 | `v0.4.12` | 0.11.14 | NO | ships fixed version |

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.12) | YES |

### Affects Versions Correction

- **Current (PSIRT-assigned):** RHTPA 2.0.0
- **Proposed (scoped to 2.2.x stream):** RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

The PSIRT-assigned version "RHTPA 2.0.0" is incorrect -- there is no 2.0.x version stream in the project configuration. Based on lock file analysis at pinned commits from the security matrix, the affected versions in the 2.2.x stream are 2.2.0, 2.2.1, and 2.2.2. Versions 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14 (the fixed version).

### Cross-Stream Impact (Case B)

The 2.1.x stream is also affected:
- 2.1.0 ships quinn-proto 0.11.9 (affected)
- 2.1.1 ships quinn-proto 0.11.9 (affected)
- The upstream branch `release/0.3.z` does NOT have the fix at HEAD

The 2.1.x stream is outside this issue's scope (issue is scoped to 2.2.x), so it is tracked as cross-stream impact. Preemptive remediation tasks are required for 2.1.x since no sibling CVE Jira exists for that stream.
