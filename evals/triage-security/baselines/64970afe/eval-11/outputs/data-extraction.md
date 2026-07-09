# Step 1 -- Data Extraction

## Issue: TC-8021

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1] |
| Issue Type | Vulnerability |
| Status | New |
| Affected component (label) | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 |
| Vulnerable library | tokio |
| Affected version range | versions before 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Due date | 2026-08-15 |
| Assignee | Unassigned |
| Existing comments | None |

## Custom Fields

| Custom Field | Field ID | Value |
|---|---|---|
| Upstream Affected Component | customfield_10632 | tokio |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-server |
| Stream | customfield_10832 | rhtpa-2.1 |

## Remote Links

| Title | URL | Type |
|-------|-----|------|
| GHSA-2026-tk91-v5pp | https://github.com/advisories/GHSA-2026-tk91-v5pp | GitHub Advisory |
| CVE-2026-55123 | https://www.cve.org/CVERecord?id=CVE-2026-55123 | CVE Record |
| tokio-rs/tokio#7001 | https://github.com/tokio-rs/tokio/pull/7001 | Upstream fix PR |

## Stream Scope Resolution

- Issue summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x**
- Konflux release repo: git.example.com/rhtpa/rhtpa-release.0.3.z
- Local path: /home/dev/repos/rhtpa-release.0.3.z
- This is a **scoped** issue -- triage Steps 3-8 apply only to the 2.1.x stream

## Ecosystem Detection

- Library: tokio (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Source repository: backend
- Upstream branch: `release/0.3.z`

## Deployment Context

- Affected repository from component label `pscomponent:org/rhtpa-server`: rhtpa-backend
- Deployment context: **upstream** (from Source Repositories table in CLAUDE.md)

## Existing Issue Links

No existing issue links on TC-8021.

## References

- https://github.com/advisories/GHSA-2026-tk91-v5pp
- https://rustsec.org/advisories/RUSTSEC-2026-0088.html
