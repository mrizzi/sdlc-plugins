# Step 1 -- Data Extraction

## Issue: TC-8030

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | "versions prior to the fix" (imprecise -- no precise threshold in Jira description) |
| Fixed version | "see advisory" (imprecise -- no precise threshold in Jira description) |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 |
| Due date | 2026-08-01 |
| Existing comments | None |

## Stream Scope Resolution

Summary suffix `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

Issue stream scope: **2.2.x only** (scoped issue).

## Ecosystem Detection

The vulnerable library `h2` is a Rust crate. From the 2.2.x stream's Ecosystem Mappings table:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

Detected ecosystem: **Cargo**

## Deployment Context

The affected repository `rhtpa-backend` is listed in the Source Repositories table with URL `https://github.com/rhtpa/rhtpa-backend`. No Deployment Context column is present in the table, so the default deployment context of **upstream** applies.

## Critical Data Gap

The Jira description says "versions prior to the fix" with no precise version threshold and "see advisory" for the fixed version. These values are imprecise and insufficient for version impact analysis. External CVE data enrichment (Step 1.5) is required to obtain a machine-readable fix threshold.
