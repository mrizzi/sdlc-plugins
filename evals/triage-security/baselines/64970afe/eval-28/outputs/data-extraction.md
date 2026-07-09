# Step 1 -- Data Extraction for TC-8060

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99010 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions before 0.4.5 |
| Fixed version | 0.4.5 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99010 |
| Advisory URL | (none) |
| Due date | 2026-08-15 |
| Reporter | psirt-analyst (account ID: 557058:psirt-analyst-mock-id) |
| Existing comments | (none) |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table.

- Stream: 2.2.x
- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Local Path: /home/dev/repos/rhtpa-release.0.4.z

Triage is scoped to the 2.2.x stream only. Other streams (2.1.x) will be checked for cross-stream impact in Step 8 Case B.

## Ecosystem Detection

The vulnerable library `h2` is a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, this maps to the **Cargo** ecosystem.

- Ecosystem: Cargo
- Repository: backend
- Lock File: Cargo.lock
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: release/0.4.z

## Deployment Context

The affected repository `rhtpa-backend` is listed in the Source Repositories table. No Deployment Context column is configured (backward compatibility), so the default context is **upstream**.
