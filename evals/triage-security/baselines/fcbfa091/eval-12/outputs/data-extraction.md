# Step 1 -- Data Extraction

## Issue: TC-8030

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Ecosystem | Cargo (crates.io) |
| Affected version range | **IMPRECISE** -- "versions prior to the fix" (no precise threshold in Jira description) |
| Fixed version | **IMPRECISE** -- "see advisory" (no precise version in Jira description) |
| CVSS | 7.5 (High) |
| Upstream fix PR | [hyperium/h2#800](https://github.com/hyperium/h2/pull/800) |
| Advisory URL | [GHSA-2026-r7f2-kk9p](https://github.com/advisories/GHSA-2026-r7f2-kk9p) |
| CVE record URL | [CVE-2026-48901](https://www.cve.org/CVERecord?id=CVE-2026-48901) |
| Due date | 2026-08-01 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to stream **2.2.x** in the Version Streams table from Security Configuration. The Konflux release repo for this stream is `git.example.com/rhtpa/rhtpa-release.0.4.z`.

## Ecosystem Detection

The vulnerable library `h2` is a Rust crate (crates.io). The ecosystem is **Cargo**, which is configured in the 2.2.x stream's Ecosystem Mappings table with:
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`
- Repository: backend

## Imprecise Data Warning

The Jira description does not provide a precise affected version range or fixed version. The affected range is stated as "versions prior to the fix" and the fixed version is "see advisory". External CVE data enrichment (Step 1.5) is required to obtain a machine-readable fix threshold for version impact analysis.
