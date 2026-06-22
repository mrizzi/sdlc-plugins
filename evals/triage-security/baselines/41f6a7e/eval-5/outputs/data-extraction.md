# Step 1 -- Data Extraction

## Issue: TC-8005

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x (mapped from suffix [rhtpa-2.2] to Version Streams table) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Ecosystem | RPM (system package in container image) |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 (Red Hat Security Advisory) |
| Upstream fix PR | N/A (RPM system package -- no upstream PR link) |
| Due date | 2026-08-15 |
| Existing comments | None |

## Stream Scope Resolution

- Issue summary suffix: `[rhtpa-2.2]`
- Mapped to configured Version Stream: **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`, local path: `/home/dev/repos/rhtpa-release.0.4.z`)
- Triage is scoped to the 2.2.x stream only

## Ecosystem Detection

- Library: openssl-libs
- Ecosystem: **RPM** (system package)
- Lock file: `rpms.lock.yaml` (configured in Ecosystem Mappings for the 2.2.x stream)
- Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
- Remediation path: single task (Konflux repo fix -- no upstream backport needed for RPM packages)
