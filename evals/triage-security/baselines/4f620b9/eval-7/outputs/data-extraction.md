# Step 1 -- Data Extraction: TC-8006

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches `pscomponent:` pattern from Security Configuration) |
| Product version (PSIRT-claimed) | [rhtpa-2.1] | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.1.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description |
| Fixed version | 0.11.14 | Description |
| CVSS | 7.5 (High) | Description |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Assignee | Unassigned | Issue field |
| Status | New | Issue field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x**
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.3.z`
- Local path: `/home/dev/repos/rhtpa-release.0.3.z`

The issue is **stream-scoped** to the 2.1.x stream. Steps 3-4 will be scoped to this stream only.

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Source repository: backend
- Upstream branch: `release/0.3.z`

## Existing Issue Links

The issue has the following pre-existing links (from `issuelinks` array in the `jira.get_issue` response):

| Link ID | Type | Direction | Linked Issue |
|---------|------|-----------|--------------|
| 1990401 | Related | outward (this issue -> TC-8001) | TC-8001 (CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]) |

## Remote Links

| Title | URL |
|-------|-----|
| GHSA-2026-qp73-x4mq | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE-2026-31812 | https://www.cve.org/CVERecord?id=CVE-2026-31812 |

## Version Impact (from security-matrix mock data)

Based on the security-matrix.md, the 2.1.x stream (this issue's scope) has the following quinn-proto versions:

| Version | Build Tag | quinn-proto Version | Affected? |
|---------|-----------|---------------------|-----------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES (< 0.11.14) |
| 2.1.1 | v0.3.12 | 0.11.9 | YES (< 0.11.14) |

Both versions in the 2.1.x stream ship quinn-proto 0.11.9, which is below the fix threshold of 0.11.14. All versions in this stream are affected.

For cross-stream context (2.2.x stream, tracked by sibling TC-8001):

| Version | Build Tag | quinn-proto Version | Affected? |
|---------|-----------|---------------------|-----------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES (< 0.11.14) |
| 2.2.1 | v0.4.8 | 0.11.12 | YES (< 0.11.14) |
| 2.2.2 | v0.4.9 | (retag of v0.4.8) | YES (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO (= 0.11.14, fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO (= 0.11.14, fixed) |
