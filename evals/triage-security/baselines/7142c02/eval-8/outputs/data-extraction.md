# Step 1 -- Data Extraction: TC-8010

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Issue Key | TC-8010 |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component | pscomponent:org/rhtpa-ui |
| Product Version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Stream Scope | 2.2.x (mapped to Konflux release repo `rhtpa-release.0.4.z`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable Library | axios |
| Ecosystem | npm |
| Affected Version Range | versions before 1.8.2 |
| Fixed Version (fix threshold) | 1.8.2 |
| CVSS | 8.1 (High) |
| Due Date | 2026-08-01 |
| Assignee | Unassigned |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |

## Custom Fields

| Custom Field | Field ID | Value |
|--------------|----------|-------|
| Upstream Affected Component | customfield_10632 | axios |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Issue Links

No existing issue links on TC-8010.

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the `2.2.x` Version Stream configured in CLAUDE.md (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`, local path: `/home/dev/repos/rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x only. Steps 3-4 will be scoped to this single stream.

## Ecosystem Detection

The vulnerable library is `axios`, which is an npm (JavaScript/TypeScript) package. The ecosystem is **npm**. Lock file inspection would use `package-lock.json` or equivalent, and remediation would follow the source dependency pattern (two tasks: upstream backport + downstream propagation).

## Description Summary

The axios package before version 1.8.2 is vulnerable to Server-Side Request Forgery (SSRF) via a crafted URL that bypasses hostname validation. An attacker can exploit this to make requests to internal services by crafting URLs that initially resolve to external hosts but redirect to internal services during redirect following.
