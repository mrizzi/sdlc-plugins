# Step 1 -- Data Extraction

## Issue

| Field | Value |
|-------|-------|
| Issue Key | TC-8040 |
| Issue Type | Vulnerability |
| Status | New |
| Assignee | Unassigned |

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches Component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | versions before 0.11.14 | Description |
| Fixed version | 0.11.14 | Description |
| CVSS | 7.5 (High) | Description |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote links |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote links |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Match: The suffix `rhtpa-2.2` maps to the `2.2.x` row in the Version Streams table (Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.4.z`).
- Scope: **Scoped** -- this issue covers only the 2.2.x stream. Steps 3-4 will be scoped to this single stream.

## Ecosystem Detection

- Vulnerable library: **quinn-proto**
- Detected ecosystem: **Go modules**
- Ecosystem Mappings table for stream 2.2.x lists: **Cargo**, **RPM**
- Ecosystem Mappings table for stream 2.1.x lists: **Cargo**, **RPM**

**Result: Go modules is NOT listed in any stream's Ecosystem Mappings table.**

The detected ecosystem does not match any configured ecosystem in the security matrix. Automated triage cannot proceed for this ecosystem -- lock file path, check command, and upstream branch are not configured.

## Deployment Context Lookup

- Component label: `pscomponent:org/rhtpa-server`
- Source repository match: `rhtpa-backend` in Source Repositories table
- Deployment context: `upstream` (default -- no Deployment Context column configured)
