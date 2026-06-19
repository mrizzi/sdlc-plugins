# Step 1 -- Data Extraction

## Issue Details

| Field | Value |
|-------|-------|
| Issue Key | TC-8002 |
| Summary | CVE-2026-28940 serde_json - Stack overflow on deeply nested input [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Assignee | Unassigned |
| Due Date | 2026-07-30 |

## Extracted CVE Data

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
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Upstream fix PR | Not provided in remote links |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

This issue is **stream-scoped** to the 2.2.x stream. Steps 3-4 will be scoped to versions in this stream only, though Step 2 analyzes all streams for completeness.

## Ecosystem Detection

The vulnerable library is **serde_json**, a Rust crate. Based on the Ecosystem Mappings tables in both streams' security-matrix.md files, this falls under the **Cargo** ecosystem.

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'`
- Source repository: backend (rhtpa-backend)

## References

- GitHub Advisory: https://github.com/advisories/GHSA-2026-j9r2-m5vk
- RUSTSEC Advisory: https://rustsec.org/advisories/RUSTSEC-2026-0019.html
- CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-28940
