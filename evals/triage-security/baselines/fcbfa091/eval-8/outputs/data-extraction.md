# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Jira Issue Key | TC-8010 |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | axios |
| Affected version range | versions before 1.8.2 |
| Fixed version | 1.8.2 |
| CVSS | 8.1 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| Due date | 2026-08-01 |
| Existing comments | (none) |
| Existing issue links | (none) |
| Assignee | Unassigned |
| Status | New |

## Custom Fields

| Custom Field | Field ID | Value |
|---|---|---|
| Upstream Affected Component | customfield_10632 | axios |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Matched Version Streams entry: `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`
- This issue is **stream-scoped** to 2.2.x only.

## Ecosystem Detection

- Library: axios
- Ecosystem: **npm** (JavaScript/TypeScript package)
- axios is a JavaScript HTTP client library, belonging to the npm ecosystem.

## Vulnerability Summary

A Server-Side Request Forgery (SSRF) vulnerability was found in the axios package. Versions before 1.8.2 are vulnerable to SSRF via a crafted URL that bypasses hostname validation. An attacker can exploit this to make requests to internal services by crafting a URL that initially resolves to an external host but redirects to an internal service. The fix threshold is axios >= 1.8.2.
