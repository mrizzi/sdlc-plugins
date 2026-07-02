# Step 1 -- Data Extraction

## PROPOSAL: Parsed CVE Data for TC-8005

The following data was extracted from Vulnerability issue TC-8005.

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` --> stream 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable package | openssl-libs |
| Ecosystem | RPM |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| Upstream fix PR | (none in remote links) |
| Due date | 2026-08-15 |
| Existing comments | (none) |

## Stream Scope

Issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`).

Triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable package `openssl-libs` is a system RPM package. The 2.2.x stream's Ecosystem Mappings table lists RPM with lock file `rpms.lock.yaml` and check command `git show <tag>:rpms.lock.yaml`. This is the RPM ecosystem -- remediation produces a single task (Konflux repo fix), not the two-task upstream+downstream pattern used for source dependency ecosystems.
