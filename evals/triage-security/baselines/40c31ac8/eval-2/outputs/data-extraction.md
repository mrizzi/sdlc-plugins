# Data Extraction -- TC-8002

## Step 0 -- Configuration Validation

Configuration extracted from project CLAUDE.md:

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

Matrix `Last-Updated` timestamp: 2026-06-28T10:00:00Z (4 days ago as of 2026-07-02). Within the 14-day freshness threshold. Proceeding.

## Step 1 -- Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | versions before 1.0.135 |
| Fixed version | 1.0.135 |
| CVSS | 5.3 (Medium) |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Due date | 2026-07-30 |
| Existing comments | None |
| Status | New |
| Assignee | Unassigned |

### Stream Scope Resolution

Issue summary suffix: `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux release repo: rhtpa-release.0.4.z). This issue is **stream-scoped** to 2.2.x.

### Ecosystem Detection

Library `serde_json` is a Rust crate. Ecosystem: **Cargo**. Lock file: `Cargo.lock`. Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'`.

The Cargo ecosystem is listed in the Ecosystem Mappings table for both streams.

### Step 1.7 -- Embargo Check

CVSS 5.3 (Medium) is below the embargo threshold of 7.0. Skipping embargo check.
