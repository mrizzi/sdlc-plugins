# Step 1 -- Data Extraction

## Issue: TC-8001

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |
| Assignee | Unassigned |
| Status | New |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration.

- **Issue stream scope**: 2.2.x
- **Konflux release repo**: git.example.com/rhtpa/rhtpa-release.0.4.z
- **Local path**: /home/dev/repos/rhtpa-release.0.4.z

This is a **scoped** issue -- Steps 3-4 will apply only to the 2.2.x stream. Cross-stream impact on 2.1.x will be evaluated in Case B (Step 8).

## Ecosystem Detection

- **Library**: quinn-proto
- **Ecosystem**: Cargo (Rust crate)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Source repository**: rhtpa-backend (from Ecosystem Mappings table)
- **Upstream branch**: `release/0.4.z` (for stream 2.2.x)

## Deployment Context

- **Repository**: rhtpa-backend
- **Deployment context**: upstream (default -- no Deployment Context column in Source Repositories table)

## Affects Versions Discrepancy (Preliminary)

The Jira Affects Versions field is set to **RHTPA 2.0.0**, but no 2.0.x stream exists in the Security Configuration. The configured streams are 2.1.x and 2.2.x. This discrepancy will be corrected in Step 3 (Affects Versions Correction) after the version impact analysis in Step 2 provides lock-file-backed evidence.

## Remote Links

| Link | Type |
|------|------|
| [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | GitHub Advisory |
| [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | CVE Record |
| [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Upstream fix PR |

## Vulnerability Summary

quinn-proto (Rust crate) before version 0.11.14 allows a remote attacker to cause a denial of service (DoS) by sending a QUIC transport frame that creates an excessive number of streams. The server panics when stream allocation exceeds internal limits. Fixed in version 0.11.14.
