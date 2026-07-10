# Step 1 -- Data Extraction for TC-8021

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component (label) | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed, summary suffix) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Upstream Affected Component (customfield_10632) | quinn-proto |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). This issue is **scoped** to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, this falls under the **Cargo** ecosystem:
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`

## Vulnerability Description

A vulnerability was found in quinn-proto. The quinn-proto crate before version 0.11.14 allows a remote attacker to cause a panic by sending a QUIC transport frame that creates an excessive number of streams. This vulnerability is classified as a denial of service (DoS).

The vulnerability exists because quinn-proto does not properly validate the number of streams requested in a STREAMS frame. An attacker can send a specially crafted frame that causes the server to allocate an unbounded number of stream state objects, leading to a panic when the allocation exceeds internal limits.

## Affects Versions Issue

PSIRT assigned `RHTPA 2.0.0` as the Affects Version. However, no 2.0.x stream exists in the configured Version Streams. The correct Affects Versions for the 2.2.x stream (based on lock file analysis -- see version impact table) should be the 2.2.x versions that ship quinn-proto < 0.11.14.

## Version Impact Table (Step 2)

Based on the lock file data from security-matrix-mock.md, using quinn-proto fix threshold >= 0.11.14:

### Stream 2.2.x (scoped stream)

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

### Stream 2.1.x (out-of-scope, for cross-stream awareness)

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 |

## Summary

- **Scoped stream (2.2.x)**: versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 are NOT affected (they ship the fixed version 0.11.14).
- **Cross-stream impact (2.1.x)**: all versions (2.1.0, 2.1.1) are affected. This is outside the issue's scope but relevant for Case B cross-stream notification.
- The PSIRT-assigned Affects Version (`RHTPA 2.0.0`) is incorrect -- no 2.0.x stream exists. The correct scoped Affects Versions are `RHTPA 2.2.0`, `RHTPA 2.2.1`, and `RHTPA 2.2.2`.
