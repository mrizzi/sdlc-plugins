# Step 1 -- Data Extraction

## Parsed CVE Data for TC-8051

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99002 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | rustls |
| Affected version range | versions before 0.23.5 |
| Fixed version | 0.23.5 |
| CVSS | 8.1 (High) |
| Upstream fix PR | https://github.com/rustls/rustls/pull/2100 |
| Advisory URL | -- |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99002 |
| Due date | 2026-08-01 |
| Existing comments | (none) |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Matched Version Streams row: 2.2.x at `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Issue stream scope: **scoped to 2.2.x only**

## Ecosystem Detection

- Vulnerable library: rustls (Rust crate)
- Detected ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "rustls"'`
- Upstream branch: `release/0.4.z`

## Deployment Context

- Affected repository: rhtpa-backend
- Deployment context: upstream (default -- no explicit Deployment Context column in Source Repositories)
