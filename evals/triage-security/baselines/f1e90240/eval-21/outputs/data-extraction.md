# Step 1 -- Data Extraction for TC-8020

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Existing comments | None |
| Upstream Affected Component (customfield_10632) | quinn-proto |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the configured Version Stream **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`). This issue is **stream-scoped** to 2.2.x.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The ecosystem is **Cargo**, which is listed in the Ecosystem Mappings table for both streams. The lock file is `Cargo.lock` and the check command is `git show <tag>:Cargo.lock`.

## Affects Versions Mismatch (Preliminary)

PSIRT assigned **RHTPA 2.0.0** as the Affects Versions value. There is no 2.0.x stream configured in the Version Streams table -- the configured streams are 2.1.x and 2.2.x. This is incorrect and will need correction in Step 3.

## Version Impact Analysis

Using the mock lock file data from the security matrix, the quinn-proto versions by pinned tag are:

### Stream 2.1.x (outside issue scope, but analyzed for cross-stream awareness)

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

### Stream 2.2.x (issue's scoped stream)

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | = 0.11.14 (fixed version) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | = 0.11.14 (fixed version) |

## Summary

- **Fix threshold**: quinn-proto >= 0.11.14
- **Scoped stream (2.2.x)**: versions 2.2.0, 2.2.1, and 2.2.2 are affected; versions 2.2.3 and 2.2.4 are NOT affected (already ship the fixed version)
- **Cross-stream (2.1.x)**: all versions (2.1.0, 2.1.1) are affected -- this will trigger Case B cross-stream impact handling since the issue is scoped to 2.2.x
