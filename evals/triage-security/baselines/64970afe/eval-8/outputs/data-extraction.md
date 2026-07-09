# Step 1 -- Data Extraction for TC-8010

## Extracted CVE Data

| Field | Value |
|-------|-------|
| **Issue Key** | TC-8010 |
| **CVE ID** | CVE-2026-44492 |
| **Summary** | CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2] |
| **Issue Type** | Vulnerability |
| **Status** | New |
| **Affected Component** | pscomponent:org/rhtpa-ui |
| **Upstream Affected Component** (customfield_10632) | axios |
| **PS Component** (customfield_10669) | pscomponent:org/rhtpa-ui |
| **Stream** (customfield_10832) | rhtpa-2.2 |
| **Vulnerable Library** | axios |
| **Affected Version Range** | versions before 1.8.2 |
| **Fixed Version (Fix Threshold)** | 1.8.2 |
| **CVSS Score** | 8.1 (High) |
| **PSIRT-Claimed Product Version** | RHTPA 2.2.0 (from summary suffix [rhtpa-2.2]) |
| **Affects Versions (Jira field)** | RHTPA 2.2.0 |
| **Due Date** | 2026-08-01 |
| **Assignee** | Unassigned |
| **Labels** | CVE-2026-44492, pscomponent:org/rhtpa-ui |
| **Advisory URL** | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| **CVE Record URL** | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| **Upstream Fix PR** | Not provided |
| **Existing Issue Links** | None |
| **Existing Comments** | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

This issue is **scoped** to the 2.2.x stream only. Steps 3-4 will be scoped to this single stream.

## Ecosystem Detection

The vulnerable library is **axios**, which is a JavaScript/TypeScript npm package. The ecosystem is **npm**.

Note: The security-matrix.md for the 2.2.x stream lists only Cargo and RPM ecosystems in its Ecosystem Mappings table. npm is not listed, which means automated lock file inspection via the matrix's configured check commands is not available for this ecosystem. However, the cross-CVE overlap analysis (Step 4.3) can still proceed based on related CVE Jira data.

## Vulnerability Description

axios before version 1.8.2 is vulnerable to Server-Side Request Forgery (SSRF) via a crafted URL that bypasses hostname validation. An attacker can exploit this to make requests to internal services. The vulnerability exists because axios does not properly validate the hostname in URLs when following redirects.
