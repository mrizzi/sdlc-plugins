# Step 1 -- Data Extraction

## Issue: TC-8020

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | tokio |
| Affected version range | versions before 1.42.0 |
| Fixed version | 1.42.0 |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Due date | 2026-08-15 |
| CVSS | 8.1 (High) |
| Existing comments | (none) |

## Stream Scope Resolution

- Issue summary suffix: `[rhtpa-2.2]`
- Mapped to configured Version Stream: **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)
- Issue stream scope: **rhtpa-2.2** (scoped to 2.2.x stream only)

## Ecosystem Detection

- Vulnerable library: tokio (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "tokio"'`
- Source repository: backend (rhtpa-backend)

## Custom Fields

- Upstream Affected Component (customfield_10632): tokio
- PS Component (customfield_10669): pscomponent:org/rhtpa-server
- Stream (customfield_10832): rhtpa-2.2

## Issue Links

No existing links on TC-8020.
