# Step 1 -- Data Extraction

## Parsed CVE Data

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
| Existing comments | (no comments) |
| Assignee | Unassigned |
| Status | New |

## Stream Scope Resolution

Issue summary suffix: `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`).

Configured Version Streams:

| Stream | Konflux Release Repo |
|--------|----------------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z |

Stream suffix `[rhtpa-2.2]` matches the `2.2.x` stream. Triage is **scoped** to the 2.2.x stream only. Cross-stream impact on 2.1.x will be reported via Case B (Step 8) if affected.

## Ecosystem Detection

Vulnerable library `openssl-libs` is a system RPM package. Ecosystem: **RPM**.

From the 2.2.x stream's Ecosystem Mappings:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

Investigation method: **rpms.lock.yaml** lock file inspection (RPM lock file is configured for this stream).
