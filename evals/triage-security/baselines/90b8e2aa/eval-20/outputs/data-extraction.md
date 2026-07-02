# Step 1 -- Data Extraction

## Issue: TC-8001

| Field | Value |
|-------|-------|
| **CVE ID** | CVE-2026-31812 |
| **Summary** | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| **Issue Type** | Vulnerability |
| **Status** | New |
| **Affected Component** | pscomponent:org/rhtpa-server |
| **Product Version (PSIRT-claimed)** | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| **Affects Versions (Jira field)** | RHTPA 2.0.0 |
| **Vulnerable Library** | quinn-proto |
| **Affected Version Range** | versions before 0.11.14 (< 0.11.14) |
| **Fixed Version** | 0.11.14 |
| **CVSS** | 7.5 (High) |
| **Ecosystem** | Cargo (Rust crate -- quinn-proto is a Rust crate, confirmed by the Ecosystem Mappings table in security-matrix.md which lists Cargo as the ecosystem for the backend repository with lock file `Cargo.lock`) |
| **Due Date** | 2026-07-15 |
| **Assignee** | Unassigned |
| **Upstream Fix PR** | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| **Advisory URL** | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| **CVE Record URL** | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| **Existing Comments** | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams configuration (Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.4.z). Triage is scoped to the 2.2.x stream.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The Ecosystem Mappings table in security-matrix.md for both streams lists **Cargo** as the ecosystem for the backend repository, with lock file `Cargo.lock` and check command `git show <tag>:Cargo.lock`. The ecosystem is therefore **Cargo**.

## Deployment Context Lookup

The Source Repositories table in the Security Configuration does not include a Deployment Context column. Per backward compatibility rules, all repositories default to `upstream`.
