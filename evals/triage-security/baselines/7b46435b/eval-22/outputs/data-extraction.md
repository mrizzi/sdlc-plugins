# Step 1 -- Data Extraction for TC-8021

## Step 0 -- Configuration Validation

Configuration validated from project CLAUDE.md:

| Setting | Value |
|---------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
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

Deployment context: upstream (default -- no Deployment Context column present)

## Step 0.3 -- Matrix Staleness Check

The security-matrix.md file has a `Last-Updated: 2026-06-28T10:00:00Z` timestamp. That is 5 days ago (current date 2026-07-03), which is within the 14-day freshness threshold. Proceeding without staleness warning.

## Extracted CVE Data

| Field | Value |
|-------|-------|
| Issue Key | TC-8021 |
| CVE ID | CVE-2026-31812 |
| Affected component (label) | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |
| Upstream Affected Component (customfield_10632) | quinn-proto |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: rhtpa-release.0.4.z). This issue is **stream-scoped** to 2.2.x.

Steps 3 and 4 will apply only to the 2.2.x stream for Affects Versions and remediation. Cross-stream impact on 2.1.x is handled via Case B (Step 8).

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The Ecosystem Mappings table for both streams lists **Cargo** as the ecosystem for the `backend` repository with lock file `Cargo.lock` and check command `git show <tag>:Cargo.lock`.

Ecosystem: **Cargo** (source dependency)

## Step 2 -- Version Impact Analysis

### quinn-proto versions extracted from lock files at pinned commits

**Stream 2.2.x (issue-scoped stream):**

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8: 0.11.12) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

**Stream 2.1.x (cross-stream check):**

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

### Summary

- **2.2.x stream (issue scope):** Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fixed quinn-proto 0.11.14.
- **2.1.x stream (cross-stream):** Both versions (2.1.0 and 2.1.1) are affected, shipping quinn-proto 0.11.9.

### Affects Versions Correction Needed

The PSIRT-assigned Affects Versions is `RHTPA 2.0.0`, which does not match any configured version stream. The correct Affects Versions for the 2.2.x-scoped issue are: **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2**.

Versions 2.2.3 and 2.2.4 are NOT affected (ship quinn-proto 0.11.14, the fixed version).
