# Step 1 -- Data Extraction: TC-8010

## Parsed CVE Data

| Field | Value |
|-------|-------|
| **Issue Key** | TC-8010 |
| **CVE ID** | CVE-2026-44492 |
| **Summary** | CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2] |
| **Issue Type** | Vulnerability |
| **Status** | New |
| **Affected Component (label)** | pscomponent:org/rhtpa-ui |
| **Upstream Affected Component** (customfield_10632) | axios |
| **PS Component** (customfield_10669) | pscomponent:org/rhtpa-ui |
| **Stream** (customfield_10832) | rhtpa-2.2 |
| **Vulnerable Library** | axios |
| **Affected Version Range** | versions before 1.8.2 |
| **Fixed Version (fix threshold)** | 1.8.2 |
| **CVSS** | 8.1 (High) |
| **Affects Versions (Jira field)** | RHTPA 2.2.0 |
| **Due Date** | 2026-08-01 |
| **Assignee** | Unassigned |
| **Existing Issue Links** | None |
| **Existing Comments** | None |

## Remote Links (Upstream References)

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-44492 |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration's Version Streams table.

- Stream suffix: `[rhtpa-2.2]` -> stream `2.2.x`
- Konflux Release Repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Local Path: `/home/dev/repos/rhtpa-release.0.4.z`

This issue is **stream-scoped** to 2.2.x only.

## Ecosystem Detection

The vulnerable library is **axios**, which is a JavaScript/TypeScript npm package. The ecosystem is **npm**. Lock file inspection and remediation task structure follow npm conventions (e.g., `package-lock.json` or `yarn.lock`).

## Custom Fields Relevant to Step 4.3 (Cross-CVE Overlap)

All three fields required for cross-CVE overlap detection are present on this issue:

- **customfield_10632** (Upstream Affected Component): `axios`
- **customfield_10669** (PS Component): `pscomponent:org/rhtpa-ui`
- **customfield_10832** (Stream): `rhtpa-2.2`
