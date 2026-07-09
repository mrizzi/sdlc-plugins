# Step 1 -- Data Extraction

## Issue: TC-8005

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| Upstream fix PR | -- (none in remote links) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | (none) |
| Status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Local path: `/home/dev/repos/rhtpa-release.0.4.z`

The issue is **scoped** to the 2.2.x stream. Steps 2-8 will analyze only the 2.2.x stream as the primary scope, with cross-stream impact checked for 2.1.x (Case B).

## Ecosystem Detection

- Vulnerable package: openssl-libs (RPM system package)
- Ecosystem: **RPM**
- Lock file: `rpms.lock.yaml` (configured in Ecosystem Mappings for both streams)
- Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`

RPM ecosystem produces a single remediation task (Konflux release repo fix). No upstream backport task needed.

## Deployment Context

- Affected repository: rhtpa-backend
- Deployment context: **upstream** (default -- no Deployment Context column in Source Repositories table)
