# Step 1 -- Data Extraction: TC-8010

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | axios |
| Affected version range | versions before 1.8.2 |
| Fixed version | 1.8.2 |
| Upstream fix PR | (none found in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| Due date | 2026-08-01 |
| CVSS | 8.1 (High) |
| Existing comments | (none) |
| Existing issue links | (none) |

## Custom Fields

| Custom Field | Field ID | Value |
|---|---|---|
| Upstream Affected Component | customfield_10632 | axios |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for `rhtpa-release.0.4.z`)
- Issue stream scope: **scoped to 2.2.x only**

## Ecosystem Detection

- Vulnerable library: **axios**
- Ecosystem: **npm** (JavaScript/TypeScript package)
- The npm ecosystem is determined from the library name -- axios is a well-known npm package used for HTTP requests in JavaScript/TypeScript projects.

## Deployment Context

- Affected repository from component label `pscomponent:org/rhtpa-ui`: rhtpa-ui
- Deployment context: **upstream** (not explicitly listed in Source Repositories table, so defaulting to `upstream`)
