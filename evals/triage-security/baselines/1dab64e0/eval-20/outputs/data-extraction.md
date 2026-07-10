# Step 1 -- Data Extraction

## Issue: TC-8001

### Parsed CVE Data

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
| Issue status | New |
| Assignee | Unassigned |

### Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)
- Issue is **stream-scoped** to 2.2.x only

### Ecosystem Detection

- Vulnerable library: **quinn-proto** (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Source repository: backend (per Ecosystem Mappings in security-matrix.md)
- Upstream branch: `release/0.4.z` (for 2.2.x stream)

### Deployment Context Lookup

- Affected repository: rhtpa-backend
- Deployment context: **upstream** (default -- no Deployment Context column in Source Repositories table)

### Remote Links

| Link Type | URL |
|-----------|-----|
| GitHub Advisory | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE Record | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |

### Vulnerability Description

A vulnerability was found in quinn-proto. The quinn-proto crate before version 0.11.14 allows a remote attacker to cause a panic by sending a QUIC transport frame that creates an excessive number of streams. This vulnerability is classified as a denial of service (DoS).

The vulnerability exists because quinn-proto does not properly validate the number of streams requested in a STREAMS frame. An attacker can send a specially crafted frame that causes the server to allocate an unbounded number of stream state objects, leading to a panic when the allocation exceeds internal limits.

### References

- https://github.com/advisories/GHSA-2026-qp73-x4mq
- https://rustsec.org/advisories/RUSTSEC-2026-0042.html

### Affects Versions Discrepancy (Preliminary)

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, but there is no 2.0.x version stream configured. The issue summary indicates stream 2.2.x. This will need correction in Step 3 based on lock file evidence from the version impact analysis.
