# Step 1 -- Data Extraction: TC-8006

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Stream scope | 2.1.x (mapped from suffix [rhtpa-2.1] to Version Streams table entry "2.1.x") |
| Affects Versions (Jira field) | RHTPA 2.1.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Status | New |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Existing comments | None |

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. This maps to the **Cargo** ecosystem, which is listed in the 2.1.x stream's Ecosystem Mappings table:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | Cargo.lock | git show \<tag\>:Cargo.lock | release/0.3.z |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.1]`. This maps to the **2.1.x** stream in the Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |

The issue is **scoped** to stream 2.1.x only. Steps 3 and 4 will be scoped to this stream.

## Deployment Context Lookup

The affected repository (rhtpa-backend from pscomponent:org/rhtpa-server) is found in the Source Repositories table. No Deployment Context column is present, so the default context of `upstream` is used.

## Existing Issue Links

The issue already has the following link:

| Link Type | Direction | Target Issue | Target Summary |
|-----------|-----------|--------------|----------------|
| Related | Outward (TC-8006 -> TC-8001) | TC-8001 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |

Link ID: 1990401

## Version Impact (from security-matrix.md mock data)

Using the 2.1.x stream's supportability matrix and quinn-proto versions by tag:

| Version | Build Tag | quinn-proto Version | Affected? (< 0.11.14) |
|---------|-----------|--------------------|-----------------------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES |
| 2.1.1 | v0.3.12 | 0.11.9 | YES |

All versions in the 2.1.x stream ship quinn-proto 0.11.9, which is below the fix threshold of 0.11.14. Both versions are affected.

For reference, the 2.2.x stream (sibling TC-8001's scope) shows:

| Version | Build Tag | quinn-proto Version | Affected? (< 0.11.14) |
|---------|-----------|--------------------|-----------------------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES |
| 2.2.1 | v0.4.8 | 0.11.12 | YES |
| 2.2.2 | v0.4.9 | (retag of v0.4.8 = 0.11.12) | YES (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO (fixed) |
