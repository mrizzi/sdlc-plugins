# Data Extraction: TC-8002

## CVE Information

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| GHSA | GHSA-2026-j9r2-m5vk |
| Summary | serde_json - Stack overflow on deeply nested input |
| Affected Package | serde_json |
| Ecosystem | Cargo (Rust) |
| Affected Versions | < 1.0.135 |
| Fixed Version | 1.0.135 |
| CVSS Score | 5.3 (Medium) |
| Attack Vector | Crafted deeply nested JSON payload causing unbounded recursion |
| Impact | Stack overflow and process crash (Denial of Service) |
| Fix Description | Configurable recursion limit defaulting to 128 levels of nesting |

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
| Comments | None |

## Component Mapping

- **Label pattern match**: `pscomponent:org/rhtpa-server` maps to the backend component
- **Source repository**: rhtpa-backend (Rust backend service)
- **Lock file**: `Cargo.lock` (Cargo ecosystem)
- **Check command**: `git show <tag>:Cargo.lock`

## References

- GitHub Advisory: https://github.com/advisories/GHSA-2026-j9r2-m5vk
- CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-28940
- RustSec Advisory: https://rustsec.org/advisories/RUSTSEC-2026-0019.html

## Affected Version Streams

The Jira issue explicitly lists "RHTPA 2.2.0" in Affects Versions, and the label `[rhtpa-2.2]` in the summary indicates the 2.2.x stream. However, triage must assess all supported streams:

| Stream | Konflux Release Repo | Versions to Check |
|--------|----------------------|-------------------|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0, 2.1.1 |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 |
