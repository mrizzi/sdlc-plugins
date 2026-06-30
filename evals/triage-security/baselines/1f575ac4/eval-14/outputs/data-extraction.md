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
| Upstream fix PR | -- |
| Advisory URL | RHSA-2026:4021 (https://access.redhat.com/errata/RHSA-2026:4021) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | (none) |
| Assignee | Unassigned |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream configured in Version Streams (Konflux Release Repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

Triage is scoped to the **2.2.x stream only**.

## Ecosystem Detection

The vulnerable library is **openssl-libs**, which is an RPM / system package. The ecosystem is **RPM**.

From the 2.2.x stream's Ecosystem Mappings table:
- Ecosystem: RPM
- Lock File: `rpms.lock.yaml`
- Check Command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
- Upstream Branch: -- (not applicable for RPM)

Since an RPM lock file (`rpms.lock.yaml`) is configured, the investigation method is lock file inspection supplemented by optional SBOM verification.
