# Step 1 -- Data Extraction

## Issue: TC-8020

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected component (label) | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE Record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Upstream Affected Component (customfield_10632) | quinn-proto |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table (Konflux release repo: `rhtpa-release.0.4.z`).

This issue is **stream-scoped** to **2.2.x** only. Steps 3 and 4 will be scoped to this stream.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, this falls under the **Cargo** ecosystem:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

Ecosystem: **Cargo** (source dependency). Remediation will require 2 tasks: upstream backport + downstream propagation.

## Version Impact Analysis (Step 2)

Using the mock lock file data from security-matrix-mock.md and the fix threshold of 0.11.14:

### Version Impact Table

| Stream | Version | Build Tag | quinn-proto | Affected? | Notes |
|--------|---------|-----------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.x | 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, which does not correspond to any configured version stream. There is no 2.0.x stream in the Security Configuration.

Scoped to stream 2.2.x (per issue suffix), the correct Affects Versions based on lock file evidence are:

- **Current**: `[RHTPA 2.0.0]` (incorrect -- no such stream exists)
- **Proposed**: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]` (versions in the 2.2.x stream that ship quinn-proto < 0.11.14)

Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14, which is at or above the fix threshold.

### Cross-Stream Impact

Stream 2.1.x is also affected (all versions ship quinn-proto 0.11.9), but this issue is scoped to 2.2.x. Cross-stream impact is reported as Case B in Step 8 and tracked via companion issues or preemptive remediation tasks.
