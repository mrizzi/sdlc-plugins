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
| CVSS | 7.1 (High) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| Upstream fix PR | (none) |
| Due date | 2026-08-15 |
| Existing comments | (none) |

## Stream Scope Resolution

Issue summary suffix `[rhtpa-2.2]` maps to the **2.2.x** version stream
(Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

Triage is scoped to the 2.2.x stream only. Versions from 2.1.x belong to
any companion sibling issue for that stream.

## Ecosystem Detection

The vulnerable package **openssl-libs** is a system RPM package.
Ecosystem: **RPM**.

From the 2.2.x stream's Ecosystem Mappings:

| Ecosystem | Repository | Lock File | Check Command |
|-----------|------------|-----------|---------------|
| RPM | -- | rpms.lock.yaml | `git show <tag>:rpms.lock.yaml` |

Lock file is configured (`rpms.lock.yaml`), so lock file inspection is the
primary investigation method.

## Deployment Context

The affected repository (rhtpa-backend) is listed in Source Repositories with
deployment context defaulting to `upstream` (no Deployment Context column present
in the mock configuration).
