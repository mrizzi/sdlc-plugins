# Step 1 -- Data Extraction: TC-8010

## Extracted Fields

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | axios |
| Affected version range | versions before 1.8.2 |
| Fixed version | 1.8.2 |
| Upstream fix PR | Not provided in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| Due date | 2026-08-01 |
| Existing comments | None |
| CVSS | 8.1 (High) |
| Status | New |
| Assignee | Unassigned |

## Custom Fields

| Custom Field | Value |
|-------------|-------|
| customfield_10632 (Upstream Affected Component) | axios |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui |
| customfield_10832 (Stream) | rhtpa-2.2 |

## Stream Scope Resolution

- Issue summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Local path: /home/dev/repos/rhtpa-release.0.4.z

The issue is **stream-scoped** to the 2.2.x stream only. Steps 3-7 will be
scoped to this stream.

## Ecosystem Detection

- Library: axios
- Ecosystem: **npm** (JavaScript/TypeScript package)
- The security-matrix.md Ecosystem Mappings table for the 2.2.x stream lists
  Cargo and RPM ecosystems but does not list npm. This means the axios package
  is not tracked via a lock file in the Konflux release repo's configured
  ecosystem mappings.

Note: The security-matrix.md mock data does not include npm ecosystem mappings
or axios version data. The vulnerability relates to axios (an npm package),
but the supportability matrix only tracks Cargo and RPM dependencies. This
indicates that axios is consumed by a different component (rhtpa-ui, a frontend
component) rather than the backend tracked in the matrix.

## Vulnerability Summary

CVE-2026-44492 is a Server-Side Request Forgery (SSRF) vulnerability in the
axios npm package. Versions before 1.8.2 are vulnerable because axios does not
properly validate the hostname in URLs when following redirects. An attacker can
craft a URL that initially resolves to an external host but redirects to an
internal service. The fix is to update axios to version 1.8.2 or later.
