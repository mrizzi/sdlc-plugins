# Data Extraction — TC-8002

## Step 0 — Configuration Validation

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

## Step 0.3 — Matrix Staleness Check

Matrix `Last-Updated` timestamp: `2026-06-28T10:00:00Z` (24 days ago as of 2026-07-22).

The matrix is older than 14 days. In a live triage, the user would be warned about staleness and given options to refresh, proceed, or stop. For this eval, proceeding with the current matrix.

## Step 1 — Extracted CVE Data

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
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Due date | 2026-07-30 |
| Existing comments | None |
| Status | New |
| Assignee | Unassigned |

### Stream Scope Resolution

Summary suffix `[rhtpa-2.2]` maps to stream **2.2.x** in the Version Streams table.
This issue is **scoped** to stream 2.2.x only.

### Ecosystem Detection

Library `serde_json` is a Rust crate. Ecosystem: **Cargo**.
Lock file: `Cargo.lock`, check command: `git show <tag>:Cargo.lock`.
Upstream branch: `release/0.4.z` (for stream 2.2.x).

### Deployment Context

Repository `rhtpa-backend` found in Source Repositories table. No Deployment Context column configured — defaulting to `upstream`.

## Step 1.5 — External CVE Data Enrichment

External sources (MITRE CVE API and OSV.dev) would be queried for CVE-2026-28940 in a live triage. For this eval, using Jira description data:

| Source | Affected range | Fixed version |
|--------|----------------|---------------|
| Jira description | < 1.0.135 | 1.0.135 |

Fix threshold used for version impact analysis: **1.0.135**

## Step 1.7 — Embargo Check

CVSS 5.3 (Medium) is below the embargo warning threshold (7.0). Embargo check skipped.
