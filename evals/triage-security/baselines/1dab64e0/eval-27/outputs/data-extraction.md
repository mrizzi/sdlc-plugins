# Step 1 -- Data Extraction

## Issue: TC-8051

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99002 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | rustls |
| Affected version range | versions before 0.23.5 |
| Fixed version | 0.23.5 |
| CVSS | 8.1 (High) |
| Upstream fix PR | https://github.com/rustls/rustls/pull/2100 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99002 |
| Advisory URL | -- |
| Due date | 2026-08-01 |
| Existing comments | (no comments) |

## Stream Scope Resolution

Issue summary suffix `[rhtpa-2.2]` maps to configured Version Stream **2.2.x**
(Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

Triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

Vulnerable library `rustls` is a Rust crate. Ecosystem: **Cargo**.

From the 2.2.x stream Ecosystem Mappings:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

## Deployment Context

Repository `rhtpa-backend` is listed in Source Repositories. Deployment context defaults to `upstream` (no Deployment Context column present in the Source Repositories table).
