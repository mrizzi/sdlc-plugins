# Step 1 -- Data Extraction for TC-8020

## Extracted CVE Metadata

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Status | New |
| Existing comments | None |
| Upstream Affected Component (customfield_10632) | quinn-proto |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). This issue is **scoped** to the 2.2.x stream only. Steps 3 and 4 will be scoped accordingly.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The ecosystem is **Cargo**. The Ecosystem Mappings table in the 2.2.x stream's security-matrix.md confirms:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

## Version Impact Analysis

Using the mock lock file data from security-matrix.md, the quinn-proto versions at each pinned tag are:

### Stream 2.2.x (in scope -- issue is scoped to this stream)

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Stream 2.1.x (cross-stream -- outside issue scope)

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

## Affects Versions Assessment

The PSIRT-assigned Affects Version `RHTPA 2.0.0` is **incorrect**. There is no 2.0.x stream configured. Based on lock file analysis scoped to the 2.2.x stream, the correct Affects Versions are:

- **RHTPA 2.2.0** -- quinn-proto 0.11.9 (affected)
- **RHTPA 2.2.1** -- quinn-proto 0.11.12 (affected)
- **RHTPA 2.2.2** -- retag of 2.2.1 (affected)

Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are NOT affected.

## Cross-Stream Impact

The 2.1.x stream is also affected (all versions ship quinn-proto 0.11.9, which is below the fix threshold of 0.11.14). This is a **Case B** scenario: cross-stream impact exists outside the issue's scope. The 2.1.x impact would be reported as a cross-stream notice, with proactive remediation tasks or companion issue linkage as appropriate.
