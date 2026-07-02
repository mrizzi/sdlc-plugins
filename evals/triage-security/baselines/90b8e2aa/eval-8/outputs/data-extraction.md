# Step 1 -- Data Extraction: TC-8010

## Parsed CVE Data

| Field | Value |
|-------|-------|
| **Jira Key** | TC-8010 |
| **CVE ID** | CVE-2026-44492 |
| **Summary** | CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2] |
| **Issue Type** | Vulnerability |
| **Status** | New |
| **Affected Component** | pscomponent:org/rhtpa-ui |
| **Product Version (PSIRT-claimed)** | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| **Affects Versions (Jira field)** | RHTPA 2.2.0 |
| **Vulnerable Library** | axios |
| **Affected Version Range** | versions before 1.8.2 |
| **Fixed Version (Fix Threshold)** | 1.8.2 |
| **CVSS** | 8.1 (High) |
| **Upstream Fix PR** | (not provided in remote links) |
| **Advisory URL** | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| **CVE Record URL** | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| **Due Date** | 2026-08-01 |
| **Assignee** | Unassigned |
| **Existing Comments** | None |
| **Existing Issue Links** | None |

## Custom Fields

| Custom Field | Field ID | Value |
|-------------|----------|-------|
| Upstream Affected Component | customfield_10632 | axios |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Stream Scope Resolution

- **Issue suffix**: `[rhtpa-2.2]`
- **Mapped stream**: 2.2.x (matches the Version Streams table in Security Configuration)
- **Scope**: Scoped -- analyze only the 2.2.x stream

## Ecosystem Detection

- **Library**: axios
- **Ecosystem**: npm (JavaScript/TypeScript package)
- The security-matrix.md for the 2.2.x stream lists Cargo and RPM ecosystem mappings but does not include an npm ecosystem mapping. However, the library is identified as an npm package from its name and context. The engineer should be consulted on where npm dependencies are tracked for this product (e.g., in a separate UI repository such as rhtpa-ui).

## Deployment Context Lookup

- **Repository from component label**: org/rhtpa-ui (parsed from `pscomponent:org/rhtpa-ui`)
- **Source Repositories table match**: rhtpa-ui is not listed in the Source Repositories table (only rhtpa-backend is listed)
- **Deployment context**: `upstream` (default, since repository not found in Source Repositories table)
