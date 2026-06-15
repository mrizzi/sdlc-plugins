# Data Extraction: TC-8002

## Jira Issue Fields

| Field | Value |
|-------|-------|
| Key | TC-8002 |
| Summary | CVE-2026-28940 serde_json - Stack overflow on deeply nested input [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Labels | CVE-2026-28940, pscomponent:org/rhtpa-server |
| Affects Versions | RHTPA 2.2.0 |
| Due Date | 2026-07-30 |
| Assignee | Unassigned |

## CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Advisory | GHSA-2026-j9r2-m5vk |
| Affected Package | serde_json |
| Ecosystem | Cargo (Rust) |
| Affected Versions | < 1.0.135 |
| Fixed Version | 1.0.135 |
| CVSS Score | 5.3 (Medium) |
| Vulnerability Type | Stack overflow via deeply nested JSON input |
| Impact | Unbounded recursion during deserialization leading to stack overflow and process crash (Denial of Service) |
| Fix Description | Introduces a configurable recursion limit defaulting to 128 levels of nesting |

## Component Identification

- **Component label**: pscomponent:org/rhtpa-server
- **Mapped repository**: rhtpa-backend (Rust backend service)
- **Lock file**: Cargo.lock
- **Check command**: `git show <tag>:Cargo.lock`

## References

- GitHub Advisory: https://github.com/advisories/GHSA-2026-j9r2-m5vk
- CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-28940
- RustSec Advisory: https://rustsec.org/advisories/RUSTSEC-2026-0019.html
