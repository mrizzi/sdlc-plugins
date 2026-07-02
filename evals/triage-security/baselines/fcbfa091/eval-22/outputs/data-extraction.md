# Step 1 -- Data Extraction

## Parsed CVE Data for TC-8021

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server |
| Affects Versions (PSIRT-assigned) | RHTPA 2.0.0 |
| Due Date | 2026-07-15 |
| Assignee | Unassigned |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | quinn-rs/quinn#2048 (https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | GHSA-2026-qp73-x4mq (https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Existing comments | None |
| Upstream Affected Component (customfield_10632) | quinn-proto |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). This issue is **stream-scoped** to 2.2.x only.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The 2.2.x stream's Ecosystem Mappings table lists **Cargo** as a supported ecosystem with:
- Repository: backend
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`

Ecosystem: **Cargo** (source dependency)

## Deployment Context Lookup

The component label `pscomponent:org/rhtpa-server` maps to the `rhtpa-backend` source repository in the Source Repositories table. No explicit Deployment Context column is present in the configuration, so the default context of `upstream` applies.

## Version Impact Analysis (Step 2)

Using the mock lock file data from the security matrix, the quinn-proto versions pinned at each release tag were compared against the fix threshold of 0.11.14:

### Stream 2.2.x (scoped stream)

| Product Version | Build Tag | quinn-proto Version | Affected? | Rationale |
|-----------------|-----------|---------------------|-----------|-----------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | v0.4.9 | 0.11.12 | YES | Retag of v0.4.8 -- same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed version) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed version) |

### Stream 2.1.x (cross-stream -- outside issue scope)

| Product Version | Build Tag | quinn-proto Version | Affected? | Rationale |
|-----------------|-----------|---------------------|-----------|-----------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 |

## Affects Versions Assessment

The PSIRT-assigned Affects Versions is `RHTPA 2.0.0`. There is no 2.0.x stream configured in the Version Streams table. The correct Affects Versions for the 2.2.x scoped stream, based on lock file evidence, should be: **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2**. Versions 2.2.3 and 2.2.4 ship the fixed version and are not affected.
