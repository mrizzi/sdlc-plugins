# Step 1 -- Data Extraction

## Issue: TC-8001

Fetched Vulnerability issue TC-8001 and its remote links.

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Vulnerability type | Denial of Service (DoS) -- panic on large stream counts |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Status | New |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`.

- Parsed suffix: `rhtpa-2.2` maps to stream **2.2.x**
- Matched Version Stream: **2.2.x** (Konflux repo: `rhtpa-release.0.4.z`)
- Issue stream scope: **scoped to 2.2.x only**

Steps 3 and 4 will apply only to the 2.2.x stream. However, Step 2 (Version Impact Analysis) will still check all streams (2.1.x and 2.2.x) to detect cross-stream impact (Case B).

## Ecosystem Detection

- Library: **quinn-proto** (Rust crate)
- Detected ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- Upstream branch (2.1.x): `release/0.3.z`
- Upstream branch (2.2.x): `release/0.4.z`

## Affects Versions Discrepancy (Preliminary)

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, but there is no 2.0.x stream in the configured Version Streams. The issue summary scopes it to 2.2.x. This discrepancy will be corrected in Step 3 after the version impact analysis confirms which versions are actually affected.

## Deployment Context

The affected component `pscomponent:org/rhtpa-server` maps to repository **rhtpa-backend** in the Source Repositories table. Deployment context defaults to **upstream** (no Deployment Context column present in configuration).

## Version Impact Preview (from mock lock file data)

Based on the mock lock file data provided in the security matrix, the quinn-proto versions by tag are:

| Tag | quinn-proto version | Affected? (< 0.11.14) |
|-----|---------------------|-----------------------|
| `v0.3.8` (2.1.0) | 0.11.9 | YES |
| `v0.3.12` (2.1.1) | 0.11.9 | YES |
| `v0.4.5` (2.2.0) | 0.11.9 | YES |
| `v0.4.8` (2.2.1) | 0.11.12 | YES |
| `v0.4.9` (2.2.2) | _(retag of v0.4.8)_ | YES (same as 2.2.1) |
| `v0.4.11` (2.2.3) | 0.11.14 | NO |
| `v0.4.12` (2.2.4) | 0.11.14 | NO |

### Summary

- **2.1.x stream**: All versions (2.1.0, 2.1.1) are affected -- ships quinn-proto 0.11.9
- **2.2.x stream**: Versions 2.2.0 through 2.2.2 are affected; versions 2.2.3 and 2.2.4 are NOT affected (ship fixed version 0.11.14)
- **Cross-stream impact**: The 2.1.x stream is also affected but is outside this issue's scope (scoped to 2.2.x). This triggers Case B (cross-stream impact) in Step 8.
