# Step 1 -- Data Extraction

## Issue: TC-8005

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| Upstream fix PR | -- |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| CVSS | 7.1 (High) |
| Due date | 2026-08-15 |
| Existing comments | (none) |

## Stream Scope

Issue summary suffix `[rhtpa-2.2]` maps to stream **2.2.x**, served by Konflux release repo `rhtpa-release.0.4.z`.

## Ecosystem Detection

The vulnerable library `openssl-libs` is an **RPM** (system package). The 2.2.x stream's Ecosystem Mappings table lists RPM with lock file `rpms.lock.yaml` and check command `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`.

Ecosystem: **RPM** (system package -- not Cargo).
