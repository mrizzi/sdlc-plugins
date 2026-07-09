# Step 1 -- Data Extraction for TC-8020

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 (versions before 0.11.14) | Description |
| Fixed version | 0.11.14 | Description |
| CVSS | 7.5 (High) | Description |
| Upstream fix PR | quinn-rs/quinn#2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Jira `duedate` field |
| Assignee | Unassigned | Jira `assignee` field |
| Existing comments | None | Jira comments |
| Upstream Affected Component | quinn-proto | customfield_10632 |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in Security Configuration:

- Stream: **2.2.x**
- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Local Path: /home/dev/repos/rhtpa-release.0.4.z

The issue is **scoped** to stream 2.2.x. Steps 3 and 4 will apply only to versions in the 2.2.x stream. Cross-stream impact on 2.1.x will be handled under Case B.

## Ecosystem Detection

Library: quinn-proto (Rust crate)
Ecosystem: **Cargo**

From the 2.2.x stream's Ecosystem Mappings:
- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`

Since this is a Cargo (source dependency) ecosystem, remediation will require **two tasks**: an upstream backport task and a downstream propagation subtask.

## Deployment Context Lookup

The affected repository (rhtpa-backend) is listed in Source Repositories. No Deployment Context column is present, so default to `upstream`.

## Version Impact Analysis (Step 2)

### Stream 2.2.x (issue scope)

| Version | Build Tag | quinn-proto Version | Fix Threshold (0.11.14) | Affected? |
|---------|-----------|---------------------|------------------------|-----------|
| 2.2.0 | v0.4.5 | 0.11.9 | 0.11.9 < 0.11.14 | YES |
| 2.2.1 | v0.4.8 | 0.11.12 | 0.11.12 < 0.11.14 | YES |
| 2.2.2 | v0.4.9 | _(retag of v0.4.8)_ | same as 2.2.1 | YES |
| 2.2.3 | v0.4.11 | 0.11.14 | 0.11.14 >= 0.11.14 | NO |
| 2.2.4 | v0.4.12 | 0.11.14 | 0.11.14 >= 0.11.14 | NO |

### Stream 2.1.x (cross-stream check)

| Version | Build Tag | quinn-proto Version | Fix Threshold (0.11.14) | Affected? |
|---------|-----------|---------------------|------------------------|-----------|
| 2.1.0 | v0.3.8 | 0.11.9 | 0.11.9 < 0.11.14 | YES |
| 2.1.1 | v0.3.12 | 0.11.9 | 0.11.9 < 0.11.14 | YES |

### Summary

- **Stream 2.2.x (issue scope)**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fixed version (0.11.14) and are NOT affected.
- **Stream 2.1.x (cross-stream)**: All versions (2.1.0, 2.1.1) are affected -- cross-stream impact applies (Case B).

## Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions is **incorrect**:
- Current: `[RHTPA 2.0.0]` -- RHTPA 2.0.0 does not match any configured version stream (no 2.0.x stream exists)
- Proposed (scoped to 2.2.x): `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

The versions 2.2.3 and 2.2.4 are excluded because they already ship quinn-proto 0.11.14 (the fixed version).

This correction requires engineer confirmation before Jira mutation.
