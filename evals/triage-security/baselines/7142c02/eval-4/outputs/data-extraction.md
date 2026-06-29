# Step 1 -- Data Extraction: TC-8004

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | _Unscoped_ (no stream suffix in summary) |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions before 0.4.8 |
| Fixed version | 0.4.8 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/812 |
| Advisory URL | https://github.com/advisories/GHSA-2026-kv8p-r3n7 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-33501 |
| Due date | 2026-08-01 |
| Existing comments | None |
| Status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" contains **no stream suffix** in brackets. This issue is treated as **unscoped** -- it covers all configured version streams.

Configured streams from Security Configuration:
- **2.1.x** -- Konflux release repo: rhtpa-release.0.3.z
- **2.2.x** -- Konflux release repo: rhtpa-release.0.4.z

All streams will be analyzed in Step 2.

## Ecosystem Detection

The vulnerable library is **h2**, a Rust crate. Based on the Ecosystem Mappings tables in both streams' security-matrix.md files, this falls under the **Cargo** ecosystem.

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`
- Source repository: backend (rhtpa-backend)

## Additional References

- RustSec: https://rustsec.org/advisories/RUSTSEC-2026-0055.html
- Distinct from CVE-2024-2758 (httpd CONTINUATION flood) -- this CVE specifically affects the Rust h2 library's header accumulation logic
- Fix: adds a configurable maximum header list size defaulting to 16 KiB
