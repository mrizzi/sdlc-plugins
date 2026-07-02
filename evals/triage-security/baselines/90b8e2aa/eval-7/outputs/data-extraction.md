# Step 1 -- Data Extraction: TC-8006

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Affects Versions (Jira field) | RHTPA 2.1.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | (none in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | (none) |
| Issue status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.1]`, which maps to the **2.1.x** version stream (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.3.z`, local path: `/home/dev/repos/rhtpa-release.0.3.z`).

This issue is **stream-scoped** to 2.1.x. Steps 3-4 will be scoped to this single stream.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. The 2.1.x stream's Ecosystem Mappings table includes a **Cargo** ecosystem entry with:
- Repository: backend
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z`

Ecosystem: **Cargo** (source dependency). Remediation would require two tasks: upstream backport + downstream propagation.

## Existing Issue Links

The issue has one existing link:
- **Related** (outward): TC-8006 --> TC-8001 (CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2])
  - Link ID: 1990401
  - Type: Related
  - Direction: outward

## Remote Links

- GitHub Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq
- CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-31812

## Deployment Context

The affected repository (rhtpa-backend) has deployment context: **upstream** (from Source Repositories table in Security Configuration).
