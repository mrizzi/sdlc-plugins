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
| CVSS | 8.1 (High) |
| Upstream fix PR | (none in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| Due date | 2026-08-01 |
| Existing comments | (none) |
| Status | New |
| Assignee | Unassigned |

## Custom Fields

| Field | Value |
|-------|-------|
| customfield_10632 (Upstream Affected Component) | axios |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui |
| customfield_10832 (Stream) | rhtpa-2.2 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table row: `2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Scope: single stream (2.2.x only)

## Ecosystem Detection

- Vulnerable library: **axios** (JavaScript/TypeScript HTTP client)
- Detected ecosystem: **npm**
- Note: The security-matrix.md for the 2.2.x stream only lists Cargo and RPM ecosystems in its Ecosystem Mappings table. npm is not configured, which means automated lock file inspection via `git show` cannot determine the exact axios version pinned at each release tag. However, the cross-CVE overlap analysis in Step 4.3 can still proceed based on existing remediation task data from related CVE Jiras.

## Vulnerability Summary

CVE-2026-44492 is a Server-Side Request Forgery (SSRF) vulnerability in the axios package. Versions before 1.8.2 are vulnerable because axios does not properly validate the hostname in URLs when following redirects. An attacker can craft a URL that initially resolves to an external host but redirects to an internal service.
