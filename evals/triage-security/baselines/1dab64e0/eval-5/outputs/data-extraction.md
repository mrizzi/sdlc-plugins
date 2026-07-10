# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| Due date | 2026-08-15 |
| Existing comments | (none) |

## Stream Scope Resolution

Issue summary suffix `[rhtpa-2.2]` maps to the **2.2.x** version stream
(Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

Triage is scoped to the 2.2.x stream only. Cross-stream impact on 2.1.x
will be assessed in Step 8 (Case B).

## Ecosystem Detection

The vulnerable package `openssl-libs` is an **RPM** system package. The 2.2.x
stream's Ecosystem Mappings table includes an RPM ecosystem row with lock file
`rpms.lock.yaml` and check command `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`.

## Deployment Context

The affected repository `rhtpa-backend` is mapped in Source Repositories with
deployment context defaulting to `upstream` (no Deployment Context column present
in the mock configuration).
