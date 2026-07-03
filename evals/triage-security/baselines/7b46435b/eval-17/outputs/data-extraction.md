# Step 1 -- Data Extraction

## Issue: TC-8001

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains `[rhtpa-2.2]`, which maps to the **2.2.x** version stream
(Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

This is a **stream-scoped** issue -- Steps 3-4 are scoped to the 2.2.x stream only.
Cross-stream impact on other streams (2.1.x) is handled via Case B in Step 8.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Based on the Ecosystem Mappings
table in the security matrix, this maps to the **Cargo** ecosystem:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` (2.2.x) / `release/0.3.z` (2.1.x) |

## Deployment Context

The Source Repositories table in the project CLAUDE.md does not include a Deployment
Context column. Per backward compatibility rules, all repositories default to `upstream`.

## Affects Versions Discrepancy (Preliminary)

The Jira issue currently has Affects Versions set to **RHTPA 2.0.0**. There is no
`2.0.x` version stream configured in Security Configuration. This value appears incorrect
and will be corrected in Step 3 based on version impact analysis from Step 2.
