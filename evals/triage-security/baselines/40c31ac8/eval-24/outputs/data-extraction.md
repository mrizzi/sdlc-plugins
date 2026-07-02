# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 (versions before 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

Summary suffix: `[rhtpa-2.2]` maps to configured Version Stream **2.2.x** (Konflux release repo: rhtpa-release.0.4.z).

Issue stream scope: **2.2.x** (scoped -- Steps 3-4 apply only to this stream).

## Ecosystem Detection

Vulnerable library `quinn-proto` is a Rust crate. Ecosystem: **Cargo**.

Lock file: `Cargo.lock`
Check command: `git show <tag>:Cargo.lock`
Source repository: backend (from Ecosystem Mappings)

## Deployment Context

The Source Repositories table does not include a Deployment Context column. Per backward compatibility rules, all repositories default to `upstream`. Coordination guidance is omitted from remediation task descriptions.

## Version Impact Analysis

### Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Build Tag | quinn-proto | Affected? | Notes |
|--------|---------|-----------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | ships fixed version |

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.12) | YES |

### Affects Versions Correction (Step 3)

PSIRT-assigned Affects Versions: `[RHTPA 2.0.0]`

RHTPA 2.0.0 does not match any configured version stream (no 2.0.x stream exists). This is incorrect.

Scoped to stream 2.2.x, the correct Affects Versions based on lock file evidence:

Current: `[RHTPA 2.0.0]` --> Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14 (the fixed version).

### Cross-Stream Impact (Case B)

Stream 2.1.x is also affected (outside this issue's scope):
- 2.1.0: quinn-proto 0.11.9 (AFFECTED)
- 2.1.1: quinn-proto 0.11.9 (AFFECTED)

The upstream branch release/0.3.z does NOT have the fix -- the latest pinned tag v0.3.12 still ships quinn-proto 0.11.9.

Preemptive remediation tasks are needed for stream 2.1.x (no companion CVE Jira exists for this stream).
