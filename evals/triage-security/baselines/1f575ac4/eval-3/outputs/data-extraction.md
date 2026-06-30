# Data Extraction — TC-8003

## Step 0 — Configuration Validation

Project configuration validated from CLAUDE.md:

| Config Item | Value |
|---|---|
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

## Step 1 — Parsed CVE Data

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

### Stream Scope Resolution

Issue summary suffix `[rhtpa-2.2]` maps to configured stream **2.2.x** (Konflux release repo: rhtpa-release.0.4.z).

This issue is **stream-scoped** to the 2.2.x stream only.

### Ecosystem Detection

Library `quinn-proto` is a Rust crate. Per the Ecosystem Mappings in the 2.2.x stream's security matrix:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

Ecosystem: **Cargo** (source dependency)

## Step 2 — Version Impact Analysis (scoped to 2.2.x stream)

Using the supportability matrix for stream 2.2.x (rhtpa-release.0.4.z) and the mock lock file data for quinn-proto:

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | v0.4.9 | — | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | >= 0.11.14, fixed |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | >= 0.11.14, fixed |

**Affected versions**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
**Not affected versions**: RHTPA 2.2.3, RHTPA 2.2.4

The fix was introduced in build v0.4.11 (version 2.2.3), where quinn-proto was updated to 0.11.14.

### Cross-stream note (2.1.x stream, outside issue scope)

The 2.1.x stream is also affected (quinn-proto 0.11.9 in both 2.1.0 and 2.1.1), but this issue is scoped to 2.2.x only. The 2.1.x stream would be tracked by a separate PSIRT issue.
