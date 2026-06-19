# Step 1 -- Data Extraction

## Issue: TC-8005

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| Upstream fix PR | -- (none in remote links) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | None |
| CVSS | 7.1 (High) |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream.

From the Version Streams table in Security Configuration:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

This issue is **scoped to the 2.2.x stream only**. Steps 2-7 will analyze only versions within this stream.

## Ecosystem Detection

The vulnerable library is **openssl-libs**, which is an RPM system package (not a Cargo crate, npm package, or Go module). This is confirmed by:

1. The library name `openssl-libs` is a well-known RPM package (Red Hat Enterprise Linux system library)
2. The version format `3.0.7-28.el9_4` follows RPM versioning conventions (NEVRA: name-version-release.dist)
3. The security-matrix.md Ecosystem Mappings table for the 2.2.x stream lists RPM as an ecosystem with `rpms.lock.yaml` as the lock file

**Ecosystem: RPM**

This means:
- Lock file: `rpms.lock.yaml`
- Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
- Remediation pattern: single task (Konflux release repo fix), not the two-task upstream backport + downstream propagation flow used for source dependency ecosystems
