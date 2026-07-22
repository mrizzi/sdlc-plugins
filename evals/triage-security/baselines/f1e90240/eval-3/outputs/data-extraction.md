# Data Extraction -- TC-8003

## Step 0 -- Configuration Validation

Configuration validated from project CLAUDE.md:

| Parameter | Value |
|-----------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Local Path |
|------------|-----|------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend |

## Step 0.3 -- Matrix Staleness Check

The security-matrix.md file has a `Last-Updated: 2026-06-28T10:00:00Z` timestamp. As of today (2026-07-22), the matrix is 24 days old, which exceeds the 14-day staleness threshold. In a live triage, the engineer would be warned and asked whether to refresh, proceed, or stop. For this eval, we proceed with the current matrix data.

## Step 1 -- Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 (overdue) |
| Existing comments | None |
| Issue status | New |
| Assignee | Unassigned |

### Stream Scope Resolution

The summary suffix `[rhtpa-2.2]` maps to the **2.2.x** version stream in the configured Version Streams table. This issue is **scoped** to the 2.2.x stream only.

### Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The 2.2.x stream's Ecosystem Mappings table lists **Cargo** with:
- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`

Ecosystem: **Cargo** (source dependency)

## Step 2 -- Version Impact Analysis

### Version Impact Table

Using the mock lock file data from security-matrix-mock.md, the quinn-proto versions at each pinned tag are:

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | Outside issue scope |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | Outside issue scope |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | Fixed (>= 0.11.14) |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | Fixed (>= 0.11.14) |

Fix threshold: quinn-proto >= 0.11.14

### Scoped Impact (2.2.x only)

Within the issue's stream scope (2.2.x), the affected versions are:
- **RHTPA 2.2.0** -- ships quinn-proto 0.11.9 (AFFECTED)
- **RHTPA 2.2.1** -- ships quinn-proto 0.11.12 (AFFECTED)
- **RHTPA 2.2.2** -- retag of 2.2.1, ships quinn-proto 0.11.12 (AFFECTED)

Not affected within 2.2.x:
- **RHTPA 2.2.3** -- ships quinn-proto 0.11.14 (FIXED)
- **RHTPA 2.2.4** -- ships quinn-proto 0.11.14 (FIXED)

### Cross-Stream Impact

Stream 2.1.x (outside issue scope) is also affected:
- RHTPA 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9 (affected)

This cross-stream impact would be reported via Case B in Step 8, but is moot because TC-8003 is a duplicate (see duplicate-check.md).
