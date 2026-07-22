# Step 1 -- Data Extraction

## Issue: TC-8030

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | "versions prior to the fix" (imprecise -- no exact threshold in Jira description) |
| Fixed version | "see advisory" (imprecise -- no exact version in Jira description) |
| CVSS | 7.5 (High) |
| Due date | 2026-08-01 |
| Upstream fix PR | [hyperium/h2#800](https://github.com/hyperium/h2/pull/800) |
| Advisory URL | [GHSA-2026-r7f2-kk9p](https://github.com/advisories/GHSA-2026-r7f2-kk9p) |
| CVE record URL | [CVE-2026-48901](https://www.cve.org/CVERecord?id=CVE-2026-48901) |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the
**2.2.x** version stream in Security Configuration.

- Stream suffix: `[rhtpa-2.2]` -> stream **2.2.x**
- Konflux Release Repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Issue stream scope: **2.2.x only** (scoped issue)

## Ecosystem Detection

The vulnerable library `h2` is a Rust crate (published on crates.io). Based on the
Ecosystem Mappings tables in the security matrix, this maps to the **Cargo** ecosystem.

- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream Branch (2.1.x): `release/0.3.z`
- Upstream Branch (2.2.x): `release/0.4.z`

## Deployment Context

The affected repository `rhtpa-backend` is listed in Source Repositories with
deployment context: **upstream** (default -- no Deployment Context column present).

## Critical Field Assessment

The Jira description provides **imprecise** affected version and fix version data:
- Affected versions: "versions prior to the fix" -- no numeric threshold
- Fixed version: "see advisory" -- no specific version number

External CVE data enrichment (Step 1.5) is required to establish the precise fix
threshold for version impact analysis.
