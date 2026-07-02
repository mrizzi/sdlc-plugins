# Step 1 — Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 (versions before 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]`, which maps to configured Version Stream **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x. Steps 3 and 4 apply only to the 2.2.x stream. Cross-stream impact on 2.1.x is handled via Case B.

## Ecosystem Detection

Library: quinn-proto (Rust crate) — Ecosystem: **Cargo**

Ecosystem Mappings (from security-matrix.md):

| Stream | Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|--------|-----------|------------|-----------|---------------|-----------------|
| 2.1.x | Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| 2.2.x | Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

## Deployment Context

Source Repositories table does not have a Deployment Context column. Per backward compatibility rules, all repos default to `upstream`. Coordination guidance is omitted from remediation tasks.

## Step 0.3 — Matrix Staleness Check

Matrix `Last-Updated: 2026-06-28T10:00:00Z` — 4 days ago (within 14-day threshold). Proceeding.

## Step 2 — Version Impact Analysis

### Dependency versions extracted from lock files

| Tag | Product Version | Stream | quinn-proto version | Source |
|-----|-----------------|--------|---------------------|--------|
| `v0.3.8` | 2.1.0 | 2.1.x | 0.11.9 | `git show v0.3.8:Cargo.lock` |
| `v0.3.12` | 2.1.1 | 2.1.x | 0.11.9 | `git show v0.3.12:Cargo.lock` |
| `v0.4.5` | 2.2.0 | 2.2.x | 0.11.9 | `git show v0.4.5:Cargo.lock` |
| `v0.4.8` | 2.2.1 | 2.2.x | 0.11.12 | `git show v0.4.8:Cargo.lock` |
| `v0.4.9` | 2.2.2 | 2.2.x | — | retag of v0.4.8 (same as 2.2.1) |
| `v0.4.11` | 2.2.3 | 2.2.x | 0.11.14 | `git show v0.4.11:Cargo.lock` |
| `v0.4.12` | 2.2.4 | 2.2.x | 0.11.14 | `git show v0.4.12:Cargo.lock` |

### Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | — | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.11+) | YES |

### Stream Impact Summary

- **2.2.x (scoped stream)**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. The fix is already present in 2.2.3 and 2.2.4 (quinn-proto 0.11.14). Upstream branch `release/0.4.z` already carries the fix. No new remediation tasks are needed for this stream.
- **2.1.x (cross-stream)**: All versions (2.1.0, 2.1.1) are affected. Upstream branch `release/0.3.z` does NOT carry the fix (still at quinn-proto 0.11.9). Remediation is needed.

## Step 3 — Affects Versions Correction

Current Affects Versions: `RHTPA 2.0.0` (incorrect — RHTPA 2.0.0 does not exist in the supportability matrix)

Proposed correction (scoped to stream 2.2.x):
- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Rationale: Lock file analysis at pinned commits from security-matrix.md confirms quinn-proto versions 0.11.9 and 0.11.12 in versions 2.2.0 through 2.2.2, all below the fix threshold of 0.11.14. Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (fixed) and are excluded.

## Triage Outcome

- **2.2.x stream**: Already fixed in versions 2.2.3+ (shipped quinn-proto 0.11.14). No new remediation tasks needed. Correct Affects Versions to RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2.
- **2.1.x stream (Case B — cross-stream impact)**: All versions affected. No existing CVE Jira for 2.1.x stream. Create preemptive remediation tasks (upstream backport + downstream propagation) with `security-preemptive` label and "Related" link to TC-8001.
