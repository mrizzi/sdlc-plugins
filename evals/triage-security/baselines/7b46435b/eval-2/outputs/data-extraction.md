# Data Extraction -- TC-8002

## Step 0 -- Configuration Validation

Configuration extracted from project CLAUDE.md (claude-md-security-config.md):

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

The security-matrix.md has a `Last-Updated: 2026-06-28T10:00:00Z` timestamp.
Current date: 2026-07-03. Age: 5 days. Threshold: 14 days.

Result: **Matrix is fresh** (5 days old, under 14-day threshold). Proceeding without staleness warning.

## Step 1 -- Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | versions before 1.0.135 (< 1.0.135) |
| Fixed version | 1.0.135 |
| CVSS | 5.3 (Medium) |
| Upstream fix PR | Not provided in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Due date | 2026-07-30 |
| Existing comments | None |
| Issue status | New |
| Assignee | Unassigned |

### Stream Scope Resolution

The issue summary contains suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: rhtpa-release.0.4.z). This issue is **stream-scoped** to 2.2.x.

However, the full version impact analysis covers all streams (2.1.x and 2.2.x) to detect cross-stream impact.

### Ecosystem Detection

The vulnerable library is **serde_json**, a Rust crate. The ecosystem is **Cargo**. Both streams' Ecosystem Mappings tables confirm Cargo is a supported ecosystem with:
- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.3.z` (2.1.x stream), `release/0.4.z` (2.2.x stream)

### Step 1.7 -- Embargo Check

CVSS is 5.3 (Medium), which is below the 7.0 threshold for the embargo warning gate. No embargo policy URL is configured in the Security Configuration. Embargo check skipped.
