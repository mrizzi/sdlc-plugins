# Step 1: Data Extraction

## Vulnerability Issue

| Field | Value |
|-------|-------|
| **Issue Key** | TC-8001 |
| **Summary** | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| **CVE ID** | CVE-2026-31812 |
| **Library** | quinn-proto |
| **Affected Versions** | < 0.11.14 |
| **Fixed Version** | 0.11.14 |
| **CVSS** | 7.5 (High) |
| **Ecosystem** | Cargo |
| **Component Label** | pscomponent:org/rhtpa-server |
| **Issue Scope** | 2.2.x stream (suffix [rhtpa-2.2]) |

## Ecosystem Detection

The library `quinn-proto` is a Rust crate. From the Ecosystem Mappings in both version streams, the ecosystem is **Cargo** with the following configuration:

| Property | Value |
|----------|-------|
| Ecosystem | Cargo |
| Repository | backend |
| Lock File | `Cargo.lock` |
| Check Command | `git show <tag>:Cargo.lock` |
| Upstream Branch (2.1.x) | `release/0.3.z` |
| Upstream Branch (2.2.x) | `release/0.4.z` |

## PSIRT-Assigned Affects Versions

| Version | Notes |
|---------|-------|
| RHTPA 2.0.0 | Assigned by PSIRT (not verified against lock files; 2.0.x stream not in supportability matrix) |

## Advisory References

- [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) -- GitHub Advisory
- [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) -- CVE Record
- [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) -- Upstream fix PR
- [RUSTSEC-2026-0042](https://rustsec.org/advisories/RUSTSEC-2026-0042.html) -- RustSec Advisory
