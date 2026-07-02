# Step 1 - Data Extraction

## Issue: TC-8001

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (pattern: `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 (versions before 0.11.14) | Description |
| Fixed version | 0.11.14 | Description |
| CVSS | 7.5 (High) | Description |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote links |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote links |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote links |
| Due date | 2026-07-15 | Jira `duedate` field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

- **Summary suffix**: `[rhtpa-2.2]`
- **Mapped stream**: 2.2.x (rhtpa-release.0.4.z)
- **Scope**: Scoped to stream 2.2.x only. Steps 3 and 4 will apply only to versions within the 2.2.x stream.

## Ecosystem Detection

- **Vulnerable library**: quinn-proto
- **Detected ecosystem**: Cargo (Rust crate)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- **Upstream branch**: `release/0.4.z` (for stream 2.2.x)

The Cargo ecosystem is listed in both streams' Ecosystem Mappings tables, confirming support for automated triage.

## Deployment Context

- **Repository**: rhtpa-backend
- **Deployment context**: upstream (default, no explicit Deployment Context column in Source Repositories table)

## Affects Versions Mismatch (Preliminary)

The PSIRT-assigned Affects Versions value of **RHTPA 2.0.0** does not correspond to any configured version stream. The configured streams are 2.1.x and 2.2.x. This will need correction in Step 3 after the version impact analysis confirms which versions are actually affected.

## Version Impact Preview (from mock lock file data)

Based on the quinn-proto versions by tag in the security matrix mock data:

| Version | Stream | Tag | quinn-proto version | Affected? (< 0.11.14) |
|---------|--------|-----|---------------------|-----------------------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES |
| 2.2.2 | 2.2.x | v0.4.9 | (retag of v0.4.8) | YES (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO |

Versions 2.2.0, 2.2.1, and 2.2.2 in the scoped stream (2.2.x) are affected. Versions 2.2.3 and 2.2.4 ship the fixed version and are not affected.

The 2.1.x stream is also affected (both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9), but since this issue is scoped to 2.2.x, cross-stream impact for 2.1.x would be handled in Step 8 Case B.
