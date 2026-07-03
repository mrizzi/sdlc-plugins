# Step 1 -- Data Extraction for TC-8006

## Extracted Fields

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
| Status | New |
| Assignee | Unassigned |

## Issue Links (from Jira get_issue response)

- **Related** (outward): TC-8001 -- CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
  - Link ID: 1990401

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Parsed stream: 2.1.x
- Matched to configured Version Stream: **2.1.x** (Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.3.z)
- Issue stream scope: **2.1.x only** (scoped issue -- Steps 3-4 apply only to this stream)

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Detected ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z` (from 2.1.x stream Ecosystem Mappings)

## Deployment Context Lookup

- Affected repository from component label `pscomponent:org/rhtpa-server`: rhtpa-backend
- Source Repositories table lookup: rhtpa-backend found
- Deployment context: `upstream` (default -- no Deployment Context column in Source Repositories table)
