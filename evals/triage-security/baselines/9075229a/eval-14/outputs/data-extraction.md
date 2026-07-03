# Step 1 -- Data Extraction

## Issue: TC-8005

Parsed CVE data from Vulnerability issue TC-8005:

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
| Upstream fix PR | (none) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | (none) |

## Stream Scope Resolution

Summary suffix `[rhtpa-2.2]` maps to stream **2.2.x** in the Version Streams table.
Triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library `openssl-libs` is an RPM system package. The 2.2.x stream's
Ecosystem Mappings table includes an RPM ecosystem row with lock file `rpms.lock.yaml`
and check command `git show <tag>:rpms.lock.yaml`.

Ecosystem: **RPM** (system package)

## Deployment Context Lookup

The affected component `org/rhtpa-server` maps to repository `rhtpa-backend` in the
Source Repositories table. No Deployment Context column is present in the Source
Repositories table (backward compatibility) -- coordination guidance will be omitted.
