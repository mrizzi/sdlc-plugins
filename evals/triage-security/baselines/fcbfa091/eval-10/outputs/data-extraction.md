# Data Extraction — TC-8020

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Issue Key | TC-8020 |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component | pscomponent:org/rhtpa-server |
| Stream Suffix | [rhtpa-2.2] |
| Stream Scope | 2.2.x (rhtpa-2.2) |
| Vulnerable Library | tokio |
| Ecosystem | Cargo |
| Affected Version Range | versions before 1.42.0 |
| Fixed Version | 1.42.0 |
| CVSS | 8.1 (High) |
| Affects Versions (PSIRT-claimed) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Due Date | 2026-08-15 |
| Assignee | Unassigned |
| Upstream Fix PR | https://github.com/tokio-rs/tokio/pull/7001 |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Additional Reference | https://rustsec.org/advisories/RUSTSEC-2026-0088.html |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the configured Version Stream `2.2.x` (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

## Ecosystem Detection

The vulnerable library `tokio` is a Rust crate. The Ecosystem Mappings table for each stream lists **Cargo** as a configured ecosystem with:

| Stream | Repository | Lock File | Check Command | Upstream Branch |
|--------|------------|-----------|---------------|-----------------|
| 2.1.x | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| 2.2.x | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

Since tokio is a source dependency (Cargo ecosystem), remediation requires two tasks per stream: an upstream backport task and a downstream propagation subtask.

## Deployment Context

The source repository `rhtpa-backend` is listed in Source Repositories without an explicit Deployment Context column. Per backward compatibility rules, the deployment context defaults to `upstream`.
