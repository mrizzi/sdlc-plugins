# Step 1 — Data Extraction

## Issue: TC-8005

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x (mapped from summary suffix [rhtpa-2.2] to Version Streams table) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Ecosystem | RPM |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`). Triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable package `openssl-libs` is an RPM system package. The 2.2.x stream's Ecosystem Mappings table includes:

| Ecosystem | Repository | Lock File | Check Command |
|-----------|------------|-----------|---------------|
| RPM | — | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml \| grep 'openssl-libs'` |

Since an RPM lock file (`rpms.lock.yaml`) is configured for this stream, the primary classification method is lock file inspection, with optional SBOM verification via cosign.
