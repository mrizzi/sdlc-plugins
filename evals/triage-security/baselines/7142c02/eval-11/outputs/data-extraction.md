# Step 1 -- Data Extraction: TC-8021

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Issue Key | TC-8021 |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1] |
| Issue Type | Vulnerability |
| Status | New |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.1 (from summary suffix `[rhtpa-2.1]`) |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 |
| Vulnerable library | tokio |
| Affected version range | versions before 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Due date | 2026-08-15 |
| Assignee | Unassigned |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x**
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.3.z`
- Local path: `/home/dev/repos/rhtpa-release.0.3.z`
- This issue is **stream-scoped** to 2.1.x only.

## Ecosystem Detection

- Library: tokio (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Source repository: rhtpa-backend (`release/0.3.z` branch for 2.1.x stream)

## Custom Fields

| Custom Field | Field ID | Value |
|---|---|---|
| Upstream Affected Component | customfield_10632 | tokio |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-server |
| Stream | customfield_10832 | rhtpa-2.1 |

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |

## Issue Links

No existing issue links on TC-8021.

## Labels

- CVE-2026-55123
- pscomponent:org/rhtpa-server
