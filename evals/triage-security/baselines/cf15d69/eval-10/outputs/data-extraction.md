# Step 1 -- Data Extraction: TC-8020

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | tokio |
| Affected version range | versions before 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Upstream fix PR | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) |
| Advisory URL | [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| CVE record URL | [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) |
| Due date | 2026-08-15 |
| Existing comments | None |
| Assignee | Unassigned |
| Status | New |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped to Version Stream: **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`)
- Issue stream scope: **rhtpa-2.2** (scoped to stream 2.2.x only)

## Ecosystem Detection

- Library: tokio (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "tokio"'`
- Source repository: rhtpa-backend

## Remote Links

- [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) -- GitHub Advisory
- [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) -- CVE Record
- [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) -- Upstream fix PR

## Custom Fields

- Upstream Affected Component (customfield_10632): tokio
- PS Component (customfield_10669): pscomponent:org/rhtpa-server
- Stream (customfield_10832): rhtpa-2.2
