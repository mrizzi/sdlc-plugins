# Data Extraction — TC-8004

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | _(no stream suffix — unscoped)_ |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions before 0.4.8 |
| Fixed version | 0.4.8 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [hyperium/h2#812](https://github.com/hyperium/h2/pull/812) |
| Advisory URL | [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7) |
| CVE record URL | [CVE-2026-33501](https://www.cve.org/CVERecord?id=CVE-2026-33501) |
| Due date | 2026-08-01 |
| Existing comments | _(none)_ |

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" contains **no stream suffix** in brackets. The issue is therefore **unscoped** and covers all configured version streams:

- Stream 2.1.x (Konflux repo: rhtpa-release.0.3.z)
- Stream 2.2.x (Konflux repo: rhtpa-release.0.4.z)

Steps 2-8 will analyze both streams.

## Ecosystem Detection

The vulnerable library **h2** is a Rust crate. The ecosystem is **Cargo**, which is listed in both streams' Ecosystem Mappings tables.

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branches: `release/0.3.z` (2.1.x), `release/0.4.z` (2.2.x)

## Deployment Context Lookup

The affected repository **rhtpa-backend** is found in the Source Repositories table. The Deployment Context column is absent from the table, so the default deployment context is **upstream**.
