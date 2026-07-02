# Step 1 -- Data Extraction: TC-8002

## Extracted CVE Metadata

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | versions before 1.0.135 |
| Fixed version | 1.0.135 |
| CVSS | 5.3 (Medium) |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Due date | 2026-07-30 |
| Assignee | Unassigned |
| Status | New |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to stream **2.2.x** (Konflux release repo `rhtpa-release.0.4.z`). This issue is **stream-scoped** to 2.2.x only.

## Ecosystem Detection

The vulnerable library `serde_json` is a Rust crate. The ecosystem is **Cargo**, which is configured in both streams' Ecosystem Mappings tables with:

- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Repository: backend

## Vulnerability Description

A stack overflow vulnerability in serde_json. Versions before 1.0.135 are vulnerable to unbounded recursion during deserialization of deeply nested JSON input, leading to a process crash. The fix (1.0.135) introduces a configurable recursion limit defaulting to 128 levels of nesting.

## References

- GitHub Advisory: https://github.com/advisories/GHSA-2026-j9r2-m5vk
- RustSec: https://rustsec.org/advisories/RUSTSEC-2026-0019.html
