# Data Extraction — TC-8004

## Step 1: Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Issue Key | TC-8004 |
| Summary | CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component | `pscomponent:org/rhtpa-server` |
| Vulnerable Library | h2 |
| Affected Version Range | versions before 0.4.8 |
| Fixed Version | 0.4.8 |
| CVSS | 7.5 (High) |
| Affects Versions (PSIRT-assigned) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Due Date | 2026-08-01 |
| Assignee | Unassigned |
| Existing Comments | None |

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7) |
| CVE Record | [CVE-2026-33501](https://www.cve.org/CVERecord?id=CVE-2026-33501) |
| Upstream Fix PR | [hyperium/h2#812](https://github.com/hyperium/h2/pull/812) |

## Additional References

- https://rustsec.org/advisories/RUSTSEC-2026-0055.html

## Stream Scope Resolution

The issue summary has **no stream suffix** (no brackets like `[rhtpa-2.1]` or `[rhtpa-2.2]`). This issue is **unscoped** -- it covers all configured version streams.

Configured streams from Security Configuration:
- **2.1.x** -- Konflux release repo: `rhtpa-release.0.3.z`
- **2.2.x** -- Konflux release repo: `rhtpa-release.0.4.z`

Both streams must be analyzed in Step 2.

## Ecosystem Detection

The vulnerable library is **h2**, a Rust crate. Based on the Ecosystem Mappings in both streams' security-matrix.md files:

- **Ecosystem**: Cargo
- **Lock File**: `Cargo.lock`
- **Check Command**: `git show <tag>:Cargo.lock`
- **Repository**: backend
- **Upstream Branch**: `release/0.3.z` (2.1.x stream), `release/0.4.z` (2.2.x stream)

This is a source dependency ecosystem, so if remediation is needed, it will require two tasks per affected stream: an upstream backport task and a downstream propagation subtask.

## Vulnerability Description

A vulnerability was found in the h2 crate. Versions of h2 before 0.4.8 are vulnerable to memory exhaustion caused by a peer sending an excessive number of CONTINUATION frames following a HEADERS frame. The h2 library accumulates all CONTINUATION frame data without enforcing a size limit on the accumulated header block, allowing an attacker to consume unbounded memory on the server. The fix (in 0.4.8) adds a configurable maximum header list size that defaults to 16 KiB.

This issue is distinct from CVE-2024-2758 (httpd CONTINUATION flood) -- this CVE specifically affects the Rust h2 library's header accumulation logic.
