# Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md:

| Parameter | Value |
|-----------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | pscomponent: |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | Not configured -- Step 4.3 and Step 7 skipped |
| PS Component field | Not configured |
| Stream custom field | Not configured |
| ProdSec contact email | Not configured |
| ProdSec Jira account ID | Not configured |
| Embargo policy URL | Not configured -- Step 1.7 skipped |

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream (default -- no Deployment Context column) |

## Step 0.3 -- Matrix Staleness Check

Matrix `Last-Updated` timestamp: 2026-06-28T10:00:00Z (4 days ago as of 2026-07-02).
This is within the 14-day threshold. No staleness warning -- proceeding with current matrix.

## Step 0.7 -- Assign and Transition

PROPOSED Jira mutations:
1. Assign TC-8002 to current user
2. Transition TC-8002 from New to Assigned

# Step 1 -- Data Extraction

Parsed from Vulnerability issue TC-8002:

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
| Upstream fix PR | Not provided in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Due date | 2026-07-30 |
| Existing comments | None |
| Issue status | New |

## Stream Scope Resolution

Summary suffix: `[rhtpa-2.2]` --> maps to stream **2.2.x**
Matched Version Streams entry: 2.2.x at git.example.com/rhtpa/rhtpa-release.0.4.z

Issue stream scope: **2.2.x** (scoped issue -- Steps 3 and 4 apply to this stream only)

## Ecosystem Detection

Vulnerable library: serde_json (Rust crate)
Detected ecosystem: **Cargo**

Ecosystem Mappings for 2.2.x stream confirm Cargo is supported:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | Cargo.lock | `git show <tag>:Cargo.lock` | release/0.4.z |

## Deployment Context

Repository rhtpa-backend has no explicit Deployment Context column in Source Repositories table.
Default: **upstream**

## Step 1.5 -- External CVE Data Enrichment

(Simulated -- external APIs not called in eval mode)

Jira description data used as authoritative source:
- Affected range: versions before 1.0.135
- Fixed version: 1.0.135

## Step 1.7 -- Embargo Check

Embargo policy URL is not configured in Security Configuration.
Step 1.7 skipped.

CVSS 5.3 (Medium) is below the Critical/Important threshold (7.0) regardless.
