# Step 1 -- Data Extraction

## Issue Metadata

| Field | Value |
|-------|-------|
| Issue Key | TC-8021 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Assignee | Unassigned |
| Due Date | 2026-07-15 |

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (pattern `pscomponent:`) |
| Upstream Affected Component | quinn-proto | customfield_10632 |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) | Summary |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description |
| Fixed version | 0.11.14 | Description |
| CVSS | 7.5 (High) | Description |
| Vulnerability type | Denial of Service (DoS) -- panic on excessive stream allocation | Description |

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE Record | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table (`git.example.com/rhtpa/rhtpa-release.0.4.z`).

This issue is **scoped** to the 2.2.x stream. Steps 3 and 4 will apply only to versions within the 2.2.x stream. Cross-stream impact (e.g., 2.1.x) will be handled under Case B.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The Ecosystem Mappings tables for both streams list **Cargo** as a configured ecosystem with:
- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z` (2.2.x stream), `release/0.3.z` (2.1.x stream)

Ecosystem: **Cargo** (source dependency)

## Deployment Context Lookup

The component label `pscomponent:org/rhtpa-server` maps to the `rhtpa-backend` source repository in the Source Repositories table. No explicit Deployment Context column is present in the configuration, so the default context `upstream` applies.

## Version Impact Analysis (Step 2)

### Supportability Matrix (Aggregated)

**Stream 2.1.x** (rhtpa-release.0.3.z):

| Version | Build | Build Date | backend tag | quinn-proto version | Affected? | Notes |
|---------|-------|------------|-------------|---------------------|-----------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

**Stream 2.2.x** (rhtpa-release.0.4.z):

| Version | Build | Build Date | backend tag | quinn-proto version | Affected? | Notes |
|---------|-------|------------|-------------|---------------------|-----------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Summary

- **Affected versions**: 2.1.0, 2.1.1 (stream 2.1.x); 2.2.0, 2.2.1, 2.2.2 (stream 2.2.x)
- **Not affected versions**: 2.2.3, 2.2.4 (stream 2.2.x) -- these ship quinn-proto 0.11.14, which is the fixed version
- **Fix introduced at**: version 2.2.3 (build 0.4.11), which first included quinn-proto 0.11.14

### Affects Versions Correction Needed

The PSIRT-assigned Affects Versions `RHTPA 2.0.0` is incorrect -- there is no 2.0.x stream in the configuration. Since this issue is scoped to stream 2.2.x, the correct Affects Versions (scoped to 2.2.x) should be:
- **RHTPA 2.2.0**
- **RHTPA 2.2.1**
- **RHTPA 2.2.2**

Versions 2.2.3 and 2.2.4 are NOT affected (they ship quinn-proto 0.11.14, the fixed version). The 2.1.x versions are affected but belong to a different stream and would be tracked by a companion CVE issue (Case B cross-stream impact).
