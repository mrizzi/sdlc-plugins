# Data Extraction — TC-8010

## Parsed CVE Data

| Field | Value |
|-------|-------|
| **Issue Key** | TC-8010 |
| **CVE ID** | CVE-2026-44492 |
| **Summary** | CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2] |
| **Issue Type** | Vulnerability |
| **Status** | New |
| **Affected Component (label)** | pscomponent:org/rhtpa-ui |
| **Upstream Affected Component (customfield_10632)** | axios |
| **PS Component (customfield_10669)** | pscomponent:org/rhtpa-ui |
| **Stream (customfield_10832)** | rhtpa-2.2 |
| **Vulnerable Library** | axios |
| **Affected Version Range** | versions before 1.8.2 |
| **Fixed Version (fix threshold)** | 1.8.2 |
| **CVSS** | 8.1 (High) |
| **Affects Versions (Jira field)** | RHTPA 2.2.0 |
| **Due Date** | 2026-08-01 |
| **Assignee** | Unassigned |
| **Advisory URL** | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| **CVE Record URL** | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| **Existing Issue Links** | None |
| **Existing Comments** | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (rhtpa-release.0.4.z)
- Scope: This issue is scoped to the 2.2.x stream only

## Ecosystem Detection

- **Ecosystem**: npm (axios is a JavaScript/TypeScript package)
- The security-matrix.md Ecosystem Mappings for the 2.2.x stream do not include an npm ecosystem entry. The configured ecosystems are Cargo and RPM.
- Since npm is not mapped in the security matrix, lock file inspection via the matrix's check commands is not directly available for this ecosystem. However, the vulnerability data is clear: axios < 1.8.2 is affected, fixed version is 1.8.2.

## Vulnerability Description

The axios package before version 1.8.2 is vulnerable to Server-Side Request Forgery (SSRF) via a crafted URL that bypasses hostname validation. An attacker can exploit this to make requests to internal services. The vulnerability exists because axios does not properly validate the hostname in URLs when following redirects.
