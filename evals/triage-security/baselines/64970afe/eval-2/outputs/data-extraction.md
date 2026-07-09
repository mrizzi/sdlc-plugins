# Step 1 -- Data Extraction: TC-8002

## Extracted CVE Data

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
| Issue status | New |
| Assignee | Unassigned |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo `rhtpa-release.0.4.z`). This is a **scoped** issue -- Steps 3 and 4 apply only to versions within the 2.2.x stream.

## Ecosystem Detection

- **Library**: serde_json (Rust crate)
- **Ecosystem**: Cargo
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'`
- **Source repository**: backend (rhtpa-backend)

## Embargo Check (Step 1.7)

No Embargo policy URL is configured in Security Configuration. Step 1.7 is skipped.

Additionally, the CVSS score of 5.3 (Medium) is below the embargo threshold of 7.0. Even if an embargo policy were configured, this step would be skipped for this severity level.

## Configuration Extracted (Step 0)

| Config Item | Value |
|-------------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |

## Matrix Staleness Check (Step 0.3)

Matrix `Last-Updated: 2026-06-28T10:00:00Z` -- 11 days ago (within the 14-day threshold). No staleness warning.
