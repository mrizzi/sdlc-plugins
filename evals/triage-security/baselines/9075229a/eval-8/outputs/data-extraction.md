# Step 1 -- Data Extraction: TC-8010

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-44492 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-ui | Label matching `pscomponent:` pattern |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | axios | Description text |
| Affected version range | versions before 1.8.2 | Description text |
| Fixed version | 1.8.2 | Description text |
| CVSS | 8.1 (High) | Description text |
| Upstream fix PR | _(none found)_ | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 | Remote links |
| Due date | 2026-08-01 | Jira `duedate` field |
| Existing comments | _(none)_ | Issue comment history |

## Custom Fields

| Field | Field ID | Value |
|-------|----------|-------|
| Upstream Affected Component | customfield_10632 | axios |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Stream Scope Resolution

- Issue summary suffix: `[rhtpa-2.2]`
- Parsed stream: `2.2.x`
- Matched Version Stream from Security Configuration: **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Issue stream scope: **scoped to 2.2.x only**

Steps 2-8 are scoped to the 2.2.x stream. Versions from other streams (e.g., 2.1.x) are outside this issue's scope.

## Ecosystem Detection

- Vulnerable library: axios
- Ecosystem: **npm** (JavaScript/TypeScript package)
- The security-matrix.md Ecosystem Mappings table for the 2.2.x stream lists Cargo and RPM ecosystems. npm is not listed in the Ecosystem Mappings.

Note: In a full triage, this would trigger the unsupported ecosystem warning. However, the cross-CVE overlap analysis (Step 4.3) operates independently of ecosystem support -- it examines remediation tasks linked to related CVE Jiras regardless of ecosystem.

## Deployment Context Lookup

- Affected repository from component label: org/rhtpa-ui
- Source Repositories table does not include rhtpa-ui (only rhtpa-backend is listed)
- Default deployment context: **upstream** (fallback when repository is not found in Source Repositories table)

## Issue Links

No existing issue links on TC-8010.
