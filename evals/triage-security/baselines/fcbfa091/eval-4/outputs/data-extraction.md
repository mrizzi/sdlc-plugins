# Data Extraction — TC-8004

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Issue Key | TC-8004 |
| Summary | CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames |
| Issue Type | Vulnerability |
| Status | New |
| Affected component | pscomponent:org/rhtpa-server |
| Stream scope | Unscoped (no stream suffix) — analyze all streams |
| Vulnerable library | h2 |
| Ecosystem | Cargo |
| Affected version range | versions before 0.4.8 |
| Fixed version | 0.4.8 |
| CVSS | 7.5 (High) |
| Affects Versions (PSIRT-claimed) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Due date | 2026-08-01 |
| Assignee | Unassigned |
| Upstream fix PR | [hyperium/h2#812](https://github.com/hyperium/h2/pull/812) |
| Advisory URL | [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7) |
| CVE record URL | [CVE-2026-33501](https://www.cve.org/CVERecord?id=CVE-2026-33501) |
| Existing comments | None |

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" contains **no stream suffix** in brackets. This issue is therefore **unscoped** and covers all configured version streams:

- 2.1.x (rhtpa-release.0.3.z)
- 2.2.x (rhtpa-release.0.4.z)

## Ecosystem Detection

The vulnerable library `h2` is a Rust crate. The Ecosystem Mappings tables for both streams list **Cargo** with lock file `Cargo.lock` and check command `git show <tag>:Cargo.lock`. The Cargo ecosystem is supported in both streams.
