# Step 1 -- Data Extraction for TC-8010

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Jira Issue Key | TC-8010 |
| Summary | CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component (label) | pscomponent:org/rhtpa-ui |
| Upstream Affected Component (customfield_10632) | axios |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-ui |
| Stream (customfield_10832) | rhtpa-2.2 |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | axios |
| Affected version range | versions before 1.8.2 |
| Fixed version (fix threshold) | 1.8.2 |
| CVSS | 8.1 (High) |
| Upstream fix PR | Not provided in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| Due Date | 2026-08-01 |
| Assignee | Unassigned |
| Existing comments | None |
| Existing issue links | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. Mapping to configured Version Streams:

- `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux Release Repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`)

This issue is **scoped** to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library is **axios**, which is an **npm** (JavaScript/TypeScript) package. This is identified from the library name and the component context (rhtpa-ui is a UI component).

The security-matrix.md for the 2.2.x stream lists Ecosystem Mappings for Cargo and RPM only -- npm is not listed in the Ecosystem Mappings table. Under normal triage, this would trigger an unsupported ecosystem warning. However, the cross-CVE overlap analysis (Step 4.3) can still proceed using the Upstream Affected Component custom field, since overlap detection operates at the Jira metadata level rather than requiring lock file inspection.

## Deployment Context

The affected repository (rhtpa-ui) is not explicitly listed in the Source Repositories table in the project CLAUDE.md. Defaulting deployment context to **upstream**.
