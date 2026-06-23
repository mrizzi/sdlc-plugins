# Step 1 -- Data Extraction: TC-8011

## Parsed CVE Data

| Field | Value |
|-------|-------|
| Issue Key | TC-8011 |
| CVE ID | CVE-2026-45678 |
| Affected Component (label) | pscomponent:org/rhtpa-ui |
| Product Version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable Library | webpack |
| Affected Version Range | versions before 5.98.0 |
| Fixed Version | 5.98.0 |
| CVSS Score | 7.8 (High) |
| Upstream Fix PR | Not provided in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Due Date | 2026-08-15 |
| Status | New |
| Assignee | Unassigned |
| Existing Comments | None |
| customfield_10632 (Upstream Affected Component) | webpack |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui |
| customfield_10832 (Stream) | rhtpa-2.2 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Local path: /home/dev/repos/rhtpa-release.0.4.z

This issue is **stream-scoped** to 2.2.x only. Steps 3-4 will be scoped to that stream.

## Ecosystem Detection

- Library: webpack
- Ecosystem: **npm** (JavaScript/TypeScript package)
- The security-matrix.md for the 2.2.x stream (rhtpa-release.0.4.z) defines Ecosystem Mappings for Cargo and RPM, but does not include an npm ecosystem mapping. The PS component label `pscomponent:org/rhtpa-ui` indicates a UI component repository, which may have its own lock file (package-lock.json) not represented in the backend-focused security matrix.
- Lock file inspection would require checking the rhtpa-ui repository's package-lock.json at pinned commits.

## Vulnerability Description

A vulnerability was found in webpack. The webpack package before version 5.98.0 allows arbitrary code execution through a specially crafted loader chain configuration. An attacker with control over a project's webpack configuration can execute arbitrary code during the build process. The vulnerability exists because webpack does not properly sanitize loader paths when resolving the loader chain, allowing path traversal to execute arbitrary modules.
