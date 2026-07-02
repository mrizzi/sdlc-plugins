# Step 1 -- Data Extraction: TC-8003

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x (mapped from summary suffix [rhtpa-2.2] to Version Streams table) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | -- (none in remote links) |
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
- **Upstream branch**: `release/0.4.z` (for stream 2.2.x)

## Stream Scope Resolution

The issue summary contains suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table. This issue is **scoped** to stream 2.2.x only. Steps 3 and 4 will operate within this stream scope.

## Deployment Context

The affected repository (rhtpa-backend) is listed in Source Repositories. No Deployment Context column is present in the Security Configuration, so the deployment context defaults to `upstream`.

## Version Impact Analysis (Step 2)

Using the security matrix data for stream 2.2.x (rhtpa-release.0.4.z) and quinn-proto lock file versions:

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | v0.4.9 | 0.11.12 | YES | retag of v0.4.8, same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

**Conclusion**: Versions 2.2.0, 2.2.1, and 2.2.2 ship vulnerable quinn-proto. Versions 2.2.3 and 2.2.4 ship the fixed version (0.11.14).

## Stream 2.1.x Cross-Reference (informational)

Since the issue is scoped to 2.2.x, stream 2.1.x is not in scope for this issue. However, for completeness:

| Version | Build Tag | quinn-proto version | Affected? |
|---------|-----------|---------------------|-----------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES |
| 2.1.1 | v0.3.12 | 0.11.9 | YES |

Stream 2.1.x is also affected but would be tracked by a separate CVE Jira per PSIRT convention.
