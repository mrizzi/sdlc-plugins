# Step 1 -- Data Extraction

## Parsed CVE Data for TC-8011

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-45678 |
| Issue Key | TC-8011 |
| Issue Type | Vulnerability |
| Status | New |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Stream scope | 2.2.x |
| Vulnerable library | webpack |
| Affected version range | versions before 5.98.0 |
| Fixed version (fix threshold) | 5.98.0 |
| CVSS | 7.8 (High) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Due date | 2026-08-15 |
| Assignee | Unassigned |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Upstream fix PR | Not provided |
| Existing comments | None |

## Custom Fields

| Custom Field | Field ID | Value |
|---|---|---|
| Upstream Affected Component | customfield_10632 | webpack |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration's Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

The issue is **stream-scoped** to 2.2.x. Steps 3-7 will operate only within this stream scope.

## Ecosystem Detection

The vulnerable library is **webpack**, which is a JavaScript/npm package. The ecosystem is **npm**. This is a source dependency ecosystem, meaning remediation would produce two tasks: an upstream backport task (fix in the source repo) and a downstream propagation subtask (update the reference in the Konflux release repo).

## Vulnerability Description

A vulnerability was found in webpack. The webpack package before version 5.98.0 allows arbitrary code execution through a specially crafted loader chain configuration. An attacker with control over a project's webpack configuration can execute arbitrary code during the build process. The vulnerability exists because webpack does not properly sanitize loader paths when resolving the loader chain, allowing path traversal to execute arbitrary modules.
