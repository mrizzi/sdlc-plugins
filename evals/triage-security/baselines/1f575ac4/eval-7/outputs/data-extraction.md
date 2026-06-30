# Step 1 -- Data Extraction for TC-8006

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches `pscomponent:` pattern from Security Configuration) |
| Product version (PSIRT-claimed) | [rhtpa-2.1] | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.1.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | (none found) | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Jira `duedate` field |
| Assignee | Unassigned | Jira field |
| Status | New | Jira field |
| Existing comments | (none) | Jira comments |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x** (matches Version Streams row: 2.1.x -> rhtpa-release.0.3.z)
- Issue stream scope: **2.1.x only** (scoped issue -- Steps 3-4 apply only to this stream)

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Source repository: backend
- Upstream branch: `release/0.3.z` (for the 2.1.x stream)

## Existing Issue Links

TC-8006 already has the following links:

| Link Type | Direction | Target Issue | Target Summary |
|-----------|-----------|--------------|----------------|
| Related | outward (TC-8006 -> TC-8001) | TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |

Link ID: 1990401

## Version Impact (from mock lock file data)

For the 2.1.x stream (rhtpa-release.0.3.z):

| Version | Build Tag | quinn-proto Version | Vulnerable? (< 0.11.14) |
|---------|-----------|---------------------|-------------------------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES |
| 2.1.1 | v0.3.12 | 0.11.9 | YES |

Both versions in the 2.1.x stream ship quinn-proto 0.11.9, which is below the fix threshold of 0.11.14.

For reference (cross-stream, 2.2.x -- tracked by sibling TC-8001):

| Version | Build Tag | quinn-proto Version | Vulnerable? (< 0.11.14) |
|---------|-----------|---------------------|-------------------------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES |
| 2.2.1 | v0.4.8 | 0.11.12 | YES |
| 2.2.2 | v0.4.9 | (retag of v0.4.8) | YES (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO (fixed) |
