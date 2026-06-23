# Step 1 -- Data Extraction

## Issue: TC-8011

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-45678 |
| Affected component (label) | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | webpack |
| Affected version range | versions before 5.98.0 |
| Fixed version (fix threshold) | 5.98.0 |
| CVSS | 7.8 (High) |
| Upstream fix PR | Not provided |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Due date | 2026-08-15 |
| Existing comments | None |
| Status | New |
| Assignee | Unassigned |

## Custom Fields

| Custom Field | Field ID | Value |
|---|---|---|
| Upstream Affected Component | customfield_10632 | webpack |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration's Version Streams table. This issue is scoped to stream 2.2.x only.

Matching Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z` (local path: `/home/dev/repos/rhtpa-release.0.4.z`).

## Ecosystem Detection

The vulnerable library is **webpack**, which is a JavaScript/TypeScript package. The ecosystem is **npm**. The lock file to inspect and the check command would be determined from the stream's `security-matrix.md` Ecosystem Mappings table.

## Vulnerability Summary

A vulnerability in the webpack package (before version 5.98.0) allows arbitrary code execution through a specially crafted loader chain configuration. An attacker with control over a project's webpack configuration can execute arbitrary code during the build process. The root cause is insufficient sanitization of loader paths when resolving the loader chain, allowing path traversal to execute arbitrary modules.
