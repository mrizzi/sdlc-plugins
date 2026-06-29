# Step 1 -- Data Extraction for TC-8006

## Extracted Fields

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Stream scope | 2.1.x (maps to Konflux release repo rhtpa-release.0.3.z at /home/dev/repos/rhtpa-release.0.3.z) |
| Affects Versions (Jira field) | RHTPA 2.1.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Status | New |
| Existing comments | None |

## Ecosystem Detection

- **Ecosystem**: Cargo (Rust crate -- quinn-proto)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Source repository**: rhtpa-backend (upstream branch: `release/0.3.z` for the 2.1.x stream)

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.1]`, which maps to the **2.1.x** version stream in the Security Configuration's Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x  | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |

This issue is **stream-scoped** to 2.1.x. Steps 3-4 will be scoped to this stream only.

## Existing Issue Links

The issue has the following pre-existing links (from Jira `issuelinks` array):

| Link ID | Type | Direction | Target Issue |
|---------|------|-----------|-------------|
| 1990401 | Related | outward (TC-8006 -> TC-8001) | TC-8001 (CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]) |

## Remote Links

- GitHub Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq
- CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-31812

## Version Impact (from security-matrix mock data)

Using the 2.1.x stream supportability matrix and quinn-proto lock file data:

| Version | Build Tag | quinn-proto version | Affected? (< 0.11.14) |
|---------|-----------|---------------------|----------------------|
| 2.1.0   | v0.3.8    | 0.11.9              | YES                  |
| 2.1.1   | v0.3.12   | 0.11.9              | YES                  |

Both versions in the 2.1.x stream ship quinn-proto 0.11.9, which is below the fix threshold of 0.11.14. Both are affected.

For cross-stream reference (2.2.x stream, covered by sibling TC-8001):

| Version | Build Tag | quinn-proto version | Affected? (< 0.11.14) |
|---------|-----------|---------------------|----------------------|
| 2.2.0   | v0.4.5    | 0.11.9              | YES                  |
| 2.2.1   | v0.4.8    | 0.11.12             | YES                  |
| 2.2.2   | v0.4.9    | (retag of v0.4.8)   | YES (same as 2.2.1)  |
| 2.2.3   | v0.4.11   | 0.11.14             | NO (fixed)           |
| 2.2.4   | v0.4.12   | 0.11.14             | NO (fixed)           |
