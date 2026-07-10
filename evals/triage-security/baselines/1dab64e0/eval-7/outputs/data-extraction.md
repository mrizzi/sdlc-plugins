# Step 1 -- Data Extraction: TC-8006

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Affects Versions (Jira field) | RHTPA 2.1.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped to stream: **2.1.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.3.z`)
- This issue is **scoped** to the 2.1.x stream only.

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- Upstream branch: `release/0.3.z`
- Repository: backend

## Existing Issue Links

- **Related** (outward): TC-8001 -- CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] (Link ID: 1990401)

## Remote Links

- [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) -- GitHub Advisory
- [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) -- CVE Record

## Version Impact Table (Step 2)

Based on the security matrix mock data, the quinn-proto versions by tag are:

| Version | Tag | quinn-proto version | Affected? | Notes |
|---------|-----|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 (outside this issue's scope) |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 (outside this issue's scope) |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (outside this issue's scope) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | >= 0.11.14 |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | >= 0.11.14 |

Within this issue's scope (stream 2.1.x): **both 2.1.0 and 2.1.1 are affected**.
