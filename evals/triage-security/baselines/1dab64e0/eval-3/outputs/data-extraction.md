# Step 1 -- Data Extraction for TC-8003

## Configuration Validation (Step 0)

Project configuration validated from CLAUDE.md:

| Setting | Value |
|---------|-------|
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

## Matrix Staleness Check (Step 0.3)

Last-Updated timestamp: 2026-06-28T10:00:00Z (12 days ago, within 14-day threshold). Proceeding without staleness warning.

## Extracted CVE Data

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
| Due date | 2026-07-15 |
| Existing comments | None |
| Assignee | Unassigned |
| Status | New |

## Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo `rhtpa-release.0.4.z`). This issue is **scoped** to the 2.2.x stream only.

## Ecosystem Detection

Vulnerable library `quinn-proto` is a Rust crate. Ecosystem: **Cargo**. Lock file: `Cargo.lock`. Check command: `git show <tag>:Cargo.lock`. Upstream branch: `release/0.4.z`.

## Version Impact Analysis (Step 2)

Using mock lock file data from security-matrix-mock.md:

### All streams (full analysis):

| Version | Stream | Tag | quinn-proto version | Affected? | Notes |
|---------|--------|-----|---------------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | < 0.11.14 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Stream-scoped view (2.2.x only, per issue scope):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| RHTPA 2.2.0 | 0.11.9 | YES | |
| RHTPA 2.2.1 | 0.11.12 | YES | |
| RHTPA 2.2.2 | -- | YES | retag of 2.2.1 |
| RHTPA 2.2.3 | 0.11.14 | NO | fixed version |
| RHTPA 2.2.4 | 0.11.14 | NO | fixed version |

### Affects Versions Correction (Step 3)

PSIRT-assigned Affects Versions: `[RHTPA 2.2.0]`

Based on lock file analysis, the correct Affects Versions for the 2.2.x stream scope are: `[RHTPA 2.2.0, RHTPA 2.2.1]` (both ship quinn-proto < 0.11.14). RHTPA 2.2.2 is a retag of 2.2.1 and also affected, but whether it has a separate Jira version depends on the project's version registry. RHTPA 2.2.3 and 2.2.4 ship the fixed version 0.11.14 and are NOT affected.

Proposed correction: `Current: [RHTPA 2.2.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1]`

### Cross-stream impact (Case B consideration)

The 2.1.x stream is also affected (versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). However, since this issue is scoped to [rhtpa-2.2], the 2.1.x stream impact would normally trigger a Case B cross-stream impact comment. This is noted but superseded by the duplicate finding in Step 4.
