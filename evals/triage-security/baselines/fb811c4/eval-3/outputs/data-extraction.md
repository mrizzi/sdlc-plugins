# Data Extraction — TC-8003

## Parsed Issue Fields

| Field | Value |
|-------|-------|
| **Issue Key** | TC-8003 |
| **Summary** | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| **Issue Type** | Vulnerability |
| **Status** | New |
| **Labels** | CVE-2026-31812, pscomponent:org/rhtpa-server |
| **Affects Versions** | RHTPA 2.2.0 |
| **Due Date** | 2026-07-15 |
| **Assignee** | Unassigned |

## CVE Details

| Field | Value |
|-------|-------|
| **CVE ID** | CVE-2026-31812 |
| **Vulnerable library** | quinn-proto |
| **Affected version range** | versions before 0.11.14 (< 0.11.14) |
| **Fixed version** | 0.11.14 |
| **CVSS** | 7.5 (High) |
| **Vulnerability type** | Denial of Service (DoS) |

## Stream Scope

- **Stream suffix**: [rhtpa-2.2] (extracted from issue summary)
- **Mapped stream**: 2.2.x
- **Konflux Release Repo**: git.example.com/rhtpa/rhtpa-release.0.4.z
- **Local path**: /home/dev/repos/rhtpa-release.0.4.z

## Vulnerability Description

The quinn-proto crate before version 0.11.14 allows a remote attacker to cause a panic by sending a QUIC transport frame that creates an excessive number of streams. The vulnerability exists because quinn-proto does not properly validate the number of streams requested in a STREAMS frame. An attacker can send a specially crafted frame that causes the server to allocate an unbounded number of stream state objects, leading to a panic when the allocation exceeds internal limits.

## References

- GitHub Advisory: [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq)
- CVE Record: [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812)
- RustSec Advisory: [RUSTSEC-2026-0042](https://rustsec.org/advisories/RUSTSEC-2026-0042.html)

## Component

- **Component label**: pscomponent:org/rhtpa-server
- **Ecosystem**: Cargo (Rust)
- **Lock file**: Cargo.lock
- **Check command**: `git show <tag>:Cargo.lock`
