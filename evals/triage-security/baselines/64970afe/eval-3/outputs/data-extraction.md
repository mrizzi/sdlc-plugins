# Data Extraction -- TC-8003

## Step 0 -- Configuration Validation

Configuration validated from CLAUDE.md:

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

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream (default) |

## Step 0.3 -- Matrix Staleness Check

Matrix `Last-Updated` timestamp: 2026-06-28T10:00:00Z (11 days ago as of 2026-07-09).
This is within the 14-day threshold. Proceeding without staleness warning.

## Step 1 -- Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Ecosystem | Cargo (Rust crate) |

### Stream Scope Resolution

Issue summary suffix: `[rhtpa-2.2]`
Mapped to configured Version Stream: **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)
Issue is **stream-scoped** to 2.2.x only.

### Ecosystem Detection

Library `quinn-proto` is a Rust crate. Ecosystem: **Cargo**.
Lock file: `Cargo.lock`
Check command: `git show <tag>:Cargo.lock`
Upstream branch: `release/0.4.z`

### Deployment Context

Repository `rhtpa-backend` found in Source Repositories. Deployment context: **upstream** (default).

## Step 2 -- Version Impact Analysis

### 2.2.x Stream (rhtpa-release.0.4.z)

Using the supportability matrix and mock lock file data for quinn-proto:

| Version | Build Tag | quinn-proto Version | Fix Threshold (0.11.14) | Affected? |
|---------|-----------|---------------------|-------------------------|-----------|
| RHTPA 2.2.0 | v0.4.5 | 0.11.9 | < 0.11.14 | **YES** |
| RHTPA 2.2.1 | v0.4.8 | 0.11.12 | < 0.11.14 | **YES** |
| RHTPA 2.2.2 | v0.4.9 | 0.11.12 (retag of v0.4.8) | < 0.11.14 | **YES** (same as 2.2.1) |
| RHTPA 2.2.3 | v0.4.11 | 0.11.14 | >= 0.11.14 | **NO** (fixed) |
| RHTPA 2.2.4 | v0.4.12 | 0.11.14 | >= 0.11.14 | **NO** (fixed) |

### Cross-stream check (2.1.x, for Case B assessment)

| Version | Build Tag | quinn-proto Version | Fix Threshold (0.11.14) | Affected? |
|---------|-----------|---------------------|-------------------------|-----------|
| RHTPA 2.1.0 | v0.3.8 | 0.11.9 | < 0.11.14 | **YES** |
| RHTPA 2.1.1 | v0.3.12 | 0.11.9 | < 0.11.14 | **YES** |

### Summary

- **2.2.x stream**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Fixed starting in 2.2.3.
- **2.1.x stream**: Both versions 2.1.0 and 2.1.1 are also affected (relevant for cross-stream Case B, but not for this scoped issue).
