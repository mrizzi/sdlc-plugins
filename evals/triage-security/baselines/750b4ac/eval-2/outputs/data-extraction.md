# Step 1 -- Data Extraction

**Issue**: TC-8002
**Summary**: CVE-2026-28940 serde_json - Stack overflow on deeply nested input [rhtpa-2.2]
**Issue Type**: Vulnerability
**Status**: New
**Assignee**: Unassigned
**Due Date**: 2026-07-30

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | < 1.0.135 |
| Fixed version | 1.0.135 |
| CVSS | 5.3 (Medium) |
| Upstream fix PR | -- |
| Advisory URL | [GHSA-2026-j9r2-m5vk](https://github.com/advisories/GHSA-2026-j9r2-m5vk) |
| CVE record URL | [CVE-2026-28940](https://www.cve.org/CVERecord?id=CVE-2026-28940) |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

**Issue stream scope**: 2.2.x

**Important Rule 4**: Although the issue is scoped to 2.2.x, all supported versions across all streams must be checked in Step 2 (version impact analysis).

## Ecosystem Detection

The vulnerable library `serde_json` is a Rust crate. Per the Ecosystem Mappings in the security-matrix.md files, the ecosystem is **Cargo**.

- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'`
- **Upstream branch (2.1.x)**: `release/0.3.z`
- **Upstream branch (2.2.x)**: `release/0.4.z`
