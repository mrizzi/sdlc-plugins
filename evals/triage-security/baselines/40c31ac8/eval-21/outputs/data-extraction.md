# Step 1 -- Data Extraction for TC-8020

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (Component label pattern: `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description |
| Fixed version | 0.11.14 | Description |
| CVSS | 7.5 (High) | Description |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote links |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote links |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comments |
| Upstream Affected Component | quinn-proto | customfield_10632 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for 2.2.x at `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z` (for stream 2.2.x)

## Deployment Context Lookup

- Affected repository (from component label `pscomponent:org/rhtpa-server`): rhtpa-backend
- Source Repositories table lookup: rhtpa-backend found
- Deployment Context column: not present in Source Repositories table (no Deployment Context column)
- Default: **upstream**

## Version Impact Analysis (from mock lock file data)

Since this issue is scoped to **2.2.x**, the primary analysis covers 2.2.x versions. However, the full impact across all streams is also assessed for cross-stream detection (Step 8 Case B).

### Stream 2.2.x (in scope)

| Version | Build Tag | quinn-proto Version | Affected? (< 0.11.14) | Notes |
|---------|-----------|--------------------|-----------------------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | **YES** | |
| 2.2.1 | v0.4.8 | 0.11.12 | **YES** | |
| 2.2.2 | v0.4.9 | 0.11.12 | **YES** | Retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.11.14 | **NO** | Fixed at 0.11.14 |
| 2.2.4 | v0.4.12 | 0.11.14 | **NO** | Fixed at 0.11.14 |

### Stream 2.1.x (out of scope -- for cross-stream analysis)

| Version | Build Tag | quinn-proto Version | Affected? (< 0.11.14) | Notes |
|---------|-----------|--------------------|-----------------------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | **YES** | |
| 2.1.1 | v0.3.12 | 0.11.9 | **YES** | |

### Summary

- **2.2.x stream**: versions 2.2.0, 2.2.1, 2.2.2 are affected; versions 2.2.3, 2.2.4 are fixed
- **2.1.x stream**: versions 2.1.0, 2.1.1 are affected (cross-stream -- out of this issue's scope)
- Ecosystem: Cargo (source dependency) -- remediation requires 2 tasks: upstream backport + downstream propagation
