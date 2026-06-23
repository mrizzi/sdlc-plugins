# Step 1 -- Data Extraction

**Issue**: TC-8005
**Status**: New
**Stream scope**: 2.2.x (parsed from summary suffix `[rhtpa-2.2]`, matched to Version Streams table)
**Ecosystem**: RPM (system package -- openssl-libs is an OS-level RPM, not a source dependency)

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable package | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| Upstream fix PR | N/A (RPM system package -- fix via RHSA errata) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | None |
| Assignee | Unassigned |

## Stream Scope Resolution

The summary suffix `[rhtpa-2.2]` maps to the **2.2.x** stream in the Version Streams table:
- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Local Path: /home/dev/repos/rhtpa-release.0.4.z

Triage is scoped to the 2.2.x stream only. The 2.1.x stream is out of scope for this issue but will be checked for cross-stream impact (Step 7, Case B).

## Ecosystem Detection

openssl-libs is an RPM system package, not a source-level dependency (Cargo/npm/Go). Per the Ecosystem Mappings table for the 2.2.x stream:
- Ecosystem: RPM
- Lock File: rpms.lock.yaml
- Check Command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
- Upstream Branch: N/A (RPM packages have no upstream branch in the source repo)

This means remediation follows the system package path: a single task in the Konflux release repo (no upstream backport task needed).
