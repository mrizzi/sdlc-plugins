# Step 1 -- Data Extraction: TC-8001

## Extracted CVE Data

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

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Matches configured Version Stream: 2.2.x at `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Issue is **scoped** to stream 2.2.x only

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch (2.1.x): `release/0.3.z`
- Upstream branch (2.2.x): `release/0.4.z`

## Deployment Context Lookup

- Affected repository: rhtpa-backend
- Source Repositories entry: rhtpa-backend at https://github.com/rhtpa/rhtpa-backend
- Deployment Context column: not present in configuration (backward compatibility)
- Deployment context: default to `upstream`

## Vulnerability Description

A vulnerability was found in quinn-proto. The quinn-proto crate before version
0.11.14 allows a remote attacker to cause a panic by sending a QUIC transport
frame that creates an excessive number of streams. This vulnerability is
classified as a denial of service (DoS).

The vulnerability exists because quinn-proto does not properly validate the
number of streams requested in a STREAMS frame. An attacker can send a specially
crafted frame that causes the server to allocate an unbounded number of stream
state objects, leading to a panic when the allocation exceeds internal limits.

## Notes

- The PSIRT-assigned Affects Versions (`RHTPA 2.0.0`) appears incorrect -- there
  is no 2.0.x stream configured in the Version Streams table. Step 3 will
  correct this based on lock file evidence from Step 2.
