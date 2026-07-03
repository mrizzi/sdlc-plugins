# Step 1 -- Data Extraction

## Issue: TC-8030

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Summary | CVE-2026-48901 h2 - HTTP/2 CONTINUATION flood [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions prior to the fix (imprecise -- no specific threshold in Jira description) |
| Fixed version | see advisory (imprecise -- no specific version in Jira description) |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 |
| Due date | 2026-08-01 |
| Existing comments | (none) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to
the **2.2.x** version stream (Konflux release repo: rhtpa-release.0.4.z).

This issue is **stream-scoped** to 2.2.x only. Steps 3-8 apply to this stream,
with cross-stream analysis covering 2.1.x as well.

## Ecosystem Detection

The vulnerable library is **h2**, a Rust crate. This maps to the **Cargo**
ecosystem, which is configured in both streams' Ecosystem Mappings tables.

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream Branch (2.2.x): `release/0.4.z`
- Upstream Branch (2.1.x): `release/0.3.z`

## Imprecise Data Flag

The Jira description does not provide a precise affected version range or fixed
version for the h2 library. It states "versions prior to the fix" and "see advisory"
respectively. External CVE data enrichment (Step 1.5) is required to determine the
exact fix threshold before version impact analysis can proceed.
