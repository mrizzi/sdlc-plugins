# Step 1 -- Data Extraction: TC-8002

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | versions before 1.0.135 |
| Fixed version | 1.0.135 |
| CVSS | 5.3 (Medium) |
| Upstream fix PR | Not provided in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Due date | 2026-07-30 |
| Existing comments | None |
| Issue status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table. This issue is scoped to the 2.2.x stream only (Konflux release repo: `rhtpa-release.0.4.z`).

## Ecosystem Detection

The vulnerable library `serde_json` is a Rust crate, placing it in the **Cargo** ecosystem. Per the Ecosystem Mappings in the 2.2.x stream's security matrix:

- Repository: backend
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`

## Vulnerability Description

serde_json versions before 1.0.135 are vulnerable to a stack overflow when deserializing deeply nested JSON input. An attacker can craft a JSON payload with thousands of nested arrays or objects that causes unbounded recursion during deserialization, leading to a stack overflow and process crash. The fix (1.0.135) introduces a configurable recursion limit that defaults to 128 levels of nesting.

## References

- GitHub Advisory: https://github.com/advisories/GHSA-2026-j9r2-m5vk
- RustSec Advisory: https://rustsec.org/advisories/RUSTSEC-2026-0019.html
- CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-28940
