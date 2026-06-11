# Step 1 -- Data Extraction

## Issue

- **Key**: TC-8004
- **Summary**: CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames
- **Issue Type**: Vulnerability
- **Status**: New

## Extracted Fields

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Affected component | `pscomponent:org/rhtpa-server` |
| Vulnerable library | h2 |
| Ecosystem | Cargo |
| Affected version range | versions before 0.4.8 (< 0.4.8) |
| Fixed version | 0.4.8 |
| CVSS | 7.5 (High) |
| Affects Versions (Jira) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Due date | 2026-08-01 |
| Upstream fix PR | [hyperium/h2#812](https://github.com/hyperium/h2/pull/812) |
| Advisory URL | [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7) |
| CVE record URL | [CVE-2026-33501](https://www.cve.org/CVERecord?id=CVE-2026-33501) |

## Stream Scope

**UNSCOPED** -- the issue summary has no stream suffix in brackets. This issue covers all configured version streams (2.1.x and 2.2.x). The version impact analysis must check all streams, and remediation is created only for actually affected streams.

## Ecosystem Detection

The vulnerable library `h2` is a Rust crate. The Ecosystem Mappings tables in both streams' security-matrix.md confirm Cargo as the ecosystem, with lock file `Cargo.lock` and check command `git show <tag>:Cargo.lock`.
