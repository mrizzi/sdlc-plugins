# Step 1 -- Data Extraction

## Issue: TC-8030

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions prior to the fix (imprecise -- no explicit threshold in Jira description) |
| Fixed version | see advisory (imprecise -- no explicit version in Jira description) |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 |
| Due date | 2026-08-01 |
| Existing comments | None |

## Stream Scope Resolution

Summary suffix `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`).

This issue is **scoped** to the 2.2.x stream only. Steps 3 and 4 will apply only to 2.2.x versions.

## Ecosystem Detection

The vulnerable library `h2` is a Rust crate. The 2.2.x stream's `security-matrix.md` Ecosystem Mappings table includes:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

Ecosystem: **Cargo** (supported).

## Deployment Context

The affected repository `rhtpa-backend` is listed in Source Repositories. No explicit Deployment Context column is present in the Source Repositories table, so the default of `upstream` applies.

## Imprecise Description Flag

The Jira description provides only vague affected/fixed version information:
- Affected versions: "versions prior to the fix" -- no numeric threshold
- Fixed version: "see advisory" -- no explicit version number

External CVE data enrichment (Step 1.5) is required to resolve precise fix thresholds.
