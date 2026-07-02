# Step 1 -- Data Extraction: TC-8006

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches Component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | [rhtpa-2.1] | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.1.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | (none found) | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links -- GitHub Advisory |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links -- CVE Record |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | (none) | Issue comment history |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x** (matches Version Streams table row: Stream `2.1.x`, Konflux Release Repo `git.example.com/rhtpa/rhtpa-release.0.3.z`)
- Issue stream scope: **2.1.x only** -- Steps 3-4 are scoped to this single stream

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z`
- Remediation pattern: 2 tasks (upstream backport + downstream propagation)

## Deployment Context Lookup

- Affected repository from component label `pscomponent:org/rhtpa-server`: rhtpa-backend
- Source Repositories mapping: rhtpa-backend found in table
- Deployment Context column: absent from configuration (no column present)
- Deployment context: **upstream** (default, since Deployment Context column is absent)

## Existing Issue Links

The issue has pre-existing links (from `issuelinks` array in the `jira.get_issue` response):

| Link ID | Type | Direction | Linked Issue |
|---------|------|-----------|--------------|
| 1990401 | Related | outward (TC-8006 -> TC-8001) | TC-8001 (CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]) |

This pre-existing link data is recorded for use in Step 4.2 (cross-stream coordination) to avoid creating duplicate links.
