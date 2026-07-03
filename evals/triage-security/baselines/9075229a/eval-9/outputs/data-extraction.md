# Step 1 -- Data Extraction: TC-8011

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-45678 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-ui | Label matching `pscomponent:` pattern |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | webpack | Description text |
| Affected version range | versions before 5.98.0 | Description text |
| Fixed version | 5.98.0 | Description text |
| CVSS | 7.8 (High) | Description text |
| Upstream fix PR | _(none found)_ | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 | Remote links |
| Due date | 2026-08-15 | Issue `duedate` field |
| Existing comments | _(none)_ | Issue comment history |

## Custom Fields

| Field | Field ID | Value |
|-------|----------|-------|
| Upstream Affected Component | customfield_10632 | webpack |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Parsed stream: `2.2.x`
- Matched Version Stream: **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Issue stream scope: **scoped to 2.2.x only**

Steps 2-8 will be scoped to the 2.2.x stream. Versions from other streams (e.g., 2.1.x) belong to companion/sibling issues.

## Ecosystem Detection

- Vulnerable library: webpack
- Ecosystem: **npm** (JavaScript/TypeScript package)
- Note: The 2.2.x stream's `security-matrix.md` Ecosystem Mappings table lists Cargo and RPM but does not list npm. Per skill rules, if the ecosystem is not listed in the matrix mappings, the user should be informed that manual assessment may be required for lock file inspection. However, the CVE data extraction and cross-CVE overlap analysis (Steps 1 and 4.3) can still proceed with the data available.

## Deployment Context Lookup

- Affected repository from component label: `org/rhtpa-ui`
- Source Repositories table match: not found (table lists `rhtpa-backend` only)
- Deployment context: **upstream** (default, since repository not found in Source Repositories table)

## Issue Status

- Current status: **New** -- proceed with full triage (default path)
