# Step 1 -- Data Extraction: TC-8004

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | _(no stream suffix -- unscoped)_ |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions before 0.4.8 |
| Fixed version | 0.4.8 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [hyperium/h2#812](https://github.com/hyperium/h2/pull/812) |
| Advisory URL | [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7) |
| CVE record URL | [CVE-2026-33501](https://www.cve.org/CVERecord?id=CVE-2026-33501) |
| Due date | 2026-08-01 |
| Existing comments | _(no comments)_ |
| Assignee | Unassigned |
| Status | New |

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" contains **no stream suffix** in brackets. This issue is therefore **unscoped** and covers all configured version streams.

Configured version streams:
- **2.1.x** -- Konflux release repo: rhtpa-release.0.3.z
- **2.2.x** -- Konflux release repo: rhtpa-release.0.4.z

Both streams will be analyzed in Step 2.

## Ecosystem Detection

The vulnerable library **h2** is a Rust crate. The Ecosystem Mappings tables for both streams list **Cargo** as a supported ecosystem with:
- Repository: backend
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branches: `release/0.3.z` (2.1.x), `release/0.4.z` (2.2.x)

Ecosystem: **Cargo** (source dependency)

## Deployment Context

The affected repository (rhtpa-backend) is listed in Source Repositories. No Deployment Context column is present in the configuration, so the default context is **upstream**.
