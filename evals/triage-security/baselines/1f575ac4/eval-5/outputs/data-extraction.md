# Step 1 -- Data Extraction

**Issue**: TC-8005
**Stream Scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| Upstream fix PR | _(none -- RPM system package)_ |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | _(none)_ |
| CVSS | 7.1 (High) |

## Ecosystem Detection

**Ecosystem: RPM** (not Cargo)

openssl-libs is a system-level RPM package, not a source dependency (Cargo/npm/Go). The ecosystem is determined by the package type: openssl-libs is an RPM distributed via Red Hat repositories, present in `rpms.lock.yaml`. The Ecosystem Mappings table in the 2.2.x stream's security-matrix.md confirms RPM ecosystem with lock file `rpms.lock.yaml` and check command `git show <tag>:rpms.lock.yaml`.

## Stream Scope Resolution

Summary suffix `[rhtpa-2.2]` maps to the **2.2.x** stream in the Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

Triage is scoped to the 2.2.x stream only. Versions from other streams (e.g., 2.1.x) are not included in Affects Versions correction or remediation for this issue.
