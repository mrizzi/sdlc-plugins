# Step 1 -- Data Extraction: TC-8004

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | _(none -- unscoped, no stream suffix in summary)_ |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions before 0.4.8 (< 0.4.8) |
| Fixed version | 0.4.8 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/812 |
| Advisory URL | https://github.com/advisories/GHSA-2026-kv8p-r3n7 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-33501 |
| Due date | 2026-08-01 |
| Assignee | Unassigned |
| Existing comments | _(no comments)_ |

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" contains **no stream suffix** in brackets. This issue is therefore **unscoped** and must be analyzed across all configured version streams (2.1.x and 2.2.x).

## Ecosystem Detection

The vulnerable library is **h2**, a Rust crate. From the security-matrix.md Ecosystem Mappings tables for both streams, the matching ecosystem is:

- **Ecosystem**: Cargo
- **Repository**: backend
- **Lock File**: `Cargo.lock`
- **Check Command**: `git show <tag>:Cargo.lock`
- **Upstream Branch**: `release/0.3.z` (2.1.x stream), `release/0.4.z` (2.2.x stream)

## Step 1.5 -- External CVE Data Enrichment

### MITRE CVE API (simulated)

Query: `https://cveawg.mitre.org/api/cve/CVE-2026-33501`

Extracted data:
- Product: h2
- Affected versions: lessThan 0.4.8
- Fixed version: 0.4.8

### OSV.dev API (simulated)

Query: `https://api.osv.dev/v1/vulns/CVE-2026-33501`

Extracted data:
- Package: h2
- Ecosystem: crates.io
- Introduced: 0 (all versions)
- Fixed: 0.4.8

### Cross-validation

| Source | Affected range | Fixed version |
|--------|----------------|---------------|
| Jira description | < 0.4.8 | 0.4.8 |
| MITRE CVE API | < 0.4.8 | 0.4.8 |
| OSV.dev | < 0.4.8 | 0.4.8 |

All three sources agree. Enriched fix threshold: **0.4.8** (high confidence).

## Vulnerability Description

A vulnerability was found in the h2 crate. Versions of h2 before 0.4.8 are vulnerable to memory exhaustion caused by a peer sending an excessive number of CONTINUATION frames following a HEADERS frame. The h2 library accumulates all CONTINUATION frame data without enforcing a size limit on the accumulated header block, allowing an attacker to consume unbounded memory on the server. The fix adds a configurable maximum header list size that defaults to 16 KiB.

This issue is distinct from CVE-2024-2758 (httpd CONTINUATION flood) -- this CVE specifically affects the Rust h2 library's header accumulation logic.

## References

- https://github.com/advisories/GHSA-2026-kv8p-r3n7
- https://rustsec.org/advisories/RUSTSEC-2026-0055.html
