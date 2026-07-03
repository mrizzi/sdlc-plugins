# Data Extraction — TC-8006

## Step 1: Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Stream scope | 2.1.x (mapped from summary suffix [rhtpa-2.1] to Version Streams table row: 2.1.x) |
| Affects Versions (Jira field) | RHTPA 2.1.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Existing issue links | Related: TC-8001 (outward, link ID 1990401) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.1]`, which maps to the **2.1.x** version stream in the Security Configuration's Version Streams table (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.3.z`).

This issue is **stream-scoped** to 2.1.x only. Steps 3 and 4 will be scoped to this stream.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. The Ecosystem Mappings table for the 2.1.x stream lists **Cargo** as a configured ecosystem with:
- Repository: backend
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z`

Ecosystem: **Cargo** (source dependency)

## Deployment Context

The affected repository `rhtpa-backend` is found in the Source Repositories table. No Deployment Context column is present in the Security Configuration, so the default deployment context is **upstream**.

## Version Impact Analysis (Step 2)

Using the mock lock file data from the security matrix:

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0   | 0.11.9      | YES       | < 0.11.14, shipped via tag v0.3.8 |
| 2.1.1   | 0.11.9      | YES       | < 0.11.14, shipped via tag v0.3.12 |

Both versions in the 2.1.x stream ship quinn-proto 0.11.9, which is below the fix threshold of 0.11.14. All versions in this stream are affected.

### Cross-stream impact (for Case B awareness)

The 2.2.x stream also has affected versions:

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0   | 0.11.9      | YES       | < 0.11.14 |
| 2.2.1   | 0.11.12     | YES       | < 0.11.14 |
| 2.2.2   | (retag)     | YES       | same as 2.2.1 |
| 2.2.3   | 0.11.14     | NO        | >= 0.11.14 (fixed) |
| 2.2.4   | 0.11.14     | NO        | >= 0.11.14 (fixed) |

However, since TC-8006 is scoped to 2.1.x, the 2.2.x stream is tracked by sibling TC-8001.
