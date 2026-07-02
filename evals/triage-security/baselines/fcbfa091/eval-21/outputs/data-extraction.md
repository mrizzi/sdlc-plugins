# Step 1 -- Data Extraction for TC-8020

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Issue Key | TC-8020 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server |
| Affects Versions (PSIRT-assigned) | RHTPA 2.0.0 |
| Due Date | 2026-07-15 |
| Assignee | Unassigned |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream Affected Component (customfield_10632) | quinn-proto |

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). This issue is **stream-scoped** to 2.2.x only.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, the ecosystem is **Cargo**. The lock file is `Cargo.lock` and the check command is `git show <tag>:Cargo.lock`. The upstream branch for the backend repository is `release/0.4.z`.

## Deployment Context

The affected component label `pscomponent:org/rhtpa-server` maps to the `rhtpa-backend` source repository. Per the Source Repositories table in CLAUDE.md Security Configuration, this repository defaults to `upstream` deployment context (no explicit Deployment Context column present).

## Version Impact Analysis (Step 2)

Using the mock lock file data from security-matrix.md, the quinn-proto versions pinned at each tag are compared against the fix threshold (0.11.14):

### Stream 2.1.x (rhtpa-release.0.3.z)

| Product Version | Build Tag | quinn-proto Version | Affected? |
|-----------------|-----------|---------------------|-----------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES -- below fix threshold 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES -- below fix threshold 0.11.14 |

### Stream 2.2.x (rhtpa-release.0.4.z) -- issue-scoped stream

| Product Version | Build Tag | quinn-proto Version | Affected? |
|-----------------|-----------|---------------------|-----------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES -- below fix threshold 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES -- below fix threshold 0.11.14 |
| 2.2.2 | v0.4.9 | (retag of v0.4.8) | YES -- same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.11.14 | NO -- meets fix threshold 0.11.14 |
| 2.2.4 | v0.4.12 | 0.11.14 | NO -- meets fix threshold 0.11.14 |

## Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions is `RHTPA 2.0.0`, which is incorrect -- there is no 2.0.x stream in the configured Version Streams. Since the issue is scoped to stream 2.2.x, the corrected Affects Versions should include only affected 2.2.x versions: `RHTPA 2.2.0`, `RHTPA 2.2.1`, `RHTPA 2.2.2`. Versions 2.2.3 and 2.2.4 are not affected (quinn-proto >= 0.11.14).

The 2.1.x versions (2.1.0, 2.1.1) are also affected but belong to a different stream and would be tracked by a companion/sibling CVE issue, not this one.
