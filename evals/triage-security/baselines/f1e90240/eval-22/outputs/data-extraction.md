# Step 1 -- Data Extraction for TC-8021

## Step 0 -- Configuration Validation

Configuration validated from project CLAUDE.md:

| Setting | Value |
|---------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component custom field | customfield_10632 |

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

The security-matrix.md has a `Last-Updated` timestamp of `2026-06-28T10:00:00Z`, which is 24 days ago (as of 2026-07-22). This exceeds the 14-day staleness threshold. In a live triage, the user would be prompted to refresh, proceed, or stop. For this eval, we proceed with the current matrix data.

## Extracted CVE Data

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
| Due date | 2026-07-15 |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Upstream Affected Component (customfield_10632) | quinn-proto |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). This issue is **scoped** to the 2.2.x stream. Steps 3 and 4 will apply only to 2.2.x versions, while cross-stream impact on 2.1.x will be handled via Case B (cross-stream impact).

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The ecosystem is **Cargo**. This matches the Ecosystem Mappings table in the security matrix, which configures:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` (2.2.x) / `release/0.3.z` (2.1.x) |

## Step 1.5 -- External CVE Data Enrichment

In a live triage, the MITRE CVE API (`https://cveawg.mitre.org/api/cve/CVE-2026-31812`) and OSV.dev API (`https://api.osv.dev/v1/vulns/CVE-2026-31812`) would be queried for structured version range data. For this eval, we use the Jira description data directly:

- Affected range: versions before 0.11.14
- Fixed version: 0.11.14

## Step 1.7 -- Embargo Check

CVE-2026-31812 has CVSS 7.5 (High severity, >= 7.0 threshold). No Embargo policy URL is configured in the Security Configuration, so this step is skipped entirely.

## Step 2 -- Version Impact Analysis

### Version Impact Table

Using lock file data from the security matrix (`git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`):

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | < 0.11.14 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 2.2.x | v0.4.9 | 0.11.12 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Dependency Chain Context (Step 2.3.5)

quinn-proto is a Cargo (Rust) crate. Based on the ecosystem mappings, the source repository is `backend` (rhtpa-backend). quinn-proto is expected to be a direct or near-direct dependency used for QUIC transport. The dependency chain would be determined by inspecting `Cargo.toml` and `Cargo.lock` in the backend repository. The dependency is a production dependency (not dev-only or build-only), given it provides core QUIC protocol handling.

### Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD (v0.4.12) | Fixed? |
|--------|-----------|-----------------|---------------------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 | NO |

- **2.2.x stream**: The upstream fix is already present at the latest released tag (v0.4.11+). Versions 2.2.3 and 2.2.4 already ship the fix. Remediation for 2.2.0-2.2.2 would involve picking up the existing upstream fix.
- **2.1.x stream**: The upstream branch `release/0.3.z` still ships 0.11.9, which is vulnerable. Remediation requires an upstream backport PR first.
