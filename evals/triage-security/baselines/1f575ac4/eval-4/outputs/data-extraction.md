# Data Extraction — TC-8004

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Issue Key | TC-8004 |
| Summary | CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component | pscomponent:org/rhtpa-server |
| Stream Scope | **Unscoped** (no stream suffix in summary — covers all streams) |
| Vulnerable Library | h2 |
| Ecosystem | Cargo (Rust crate) |
| Affected Version Range | versions before 0.4.8 |
| Fixed Version | 0.4.8 |
| CVSS | 7.5 (High) |
| PSIRT Affects Versions | RHTPA 2.1.0, RHTPA 2.2.0 |
| Due Date | 2026-08-01 |
| Assignee | Unassigned |
| Labels | CVE-2026-33501, pscomponent:org/rhtpa-server |

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7) |
| CVE Record | [CVE-2026-33501](https://www.cve.org/CVERecord?id=CVE-2026-33501) |
| Upstream Fix PR | [hyperium/h2#812](https://github.com/hyperium/h2/pull/812) |

## Additional References

- https://github.com/advisories/GHSA-2026-kv8p-r3n7
- https://rustsec.org/advisories/RUSTSEC-2026-0055.html

## Ecosystem Detection

The vulnerable library `h2` is a Rust crate. Both streams' security-matrix.md Ecosystem Mappings tables list **Cargo** as the ecosystem with:
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Repository: backend

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" contains **no stream suffix** in brackets. This issue is therefore **unscoped** and covers all configured version streams (2.1.x and 2.2.x). Version impact analysis must check all streams, and remediation tasks are created only for actually affected streams.

## Vulnerability Description

A vulnerability was found in the h2 crate. Versions of h2 before 0.4.8 are vulnerable to memory exhaustion caused by a peer sending an excessive number of CONTINUATION frames following a HEADERS frame. The h2 library accumulates all CONTINUATION frame data without enforcing a size limit on the accumulated header block, allowing an attacker to consume unbounded memory on the server. The fix adds a configurable maximum header list size that defaults to 16 KiB.

This issue is distinct from CVE-2024-2758 (httpd CONTINUATION flood) — this CVE specifically affects the Rust h2 library's header accumulation logic.
