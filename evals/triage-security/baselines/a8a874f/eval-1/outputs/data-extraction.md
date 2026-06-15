# Step 1: Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Jira Key | TC-8001 |
| Summary | quinn-proto - Panic on large stream counts |
| Vulnerable Library | quinn-proto (Rust crate) |
| Affected Version Range | versions before 0.11.14 (< 0.11.14) |
| Fixed Version | 0.11.14 |
| CVSS | 7.5 (High) |
| Ecosystem | Cargo |
| Lock File | Cargo.lock |
| Stream Scope | [rhtpa-2.2] -- 2.2.x stream |
| Component | pscomponent:org/rhtpa-server |
| PSIRT Affects Versions | RHTPA 2.0.0 |

### Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. This maps to the **Cargo** ecosystem as confirmed by the Ecosystem Mappings tables in the security-matrix, which list Cargo with lock file `Cargo.lock` and check command `git show <tag>:Cargo.lock`.

### Remote Links

| Link Type | URL |
|-----------|-----|
| GitHub Advisory | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE Record | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Upstream Fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |

### Additional References

- RustSec Advisory: https://rustsec.org/advisories/RUSTSEC-2026-0042.html

### Vulnerability Description

quinn-proto before version 0.11.14 allows a remote attacker to cause a panic by sending a QUIC transport frame that creates an excessive number of streams. The vulnerability exists because quinn-proto does not properly validate the number of streams requested in a STREAMS frame. An attacker can send a specially crafted frame that causes the server to allocate an unbounded number of stream state objects, leading to a panic when the allocation exceeds internal limits. This is classified as a denial of service (DoS).
