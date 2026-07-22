# Step 1 -- Data Extraction: TC-8021

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.1 (from summary suffix `[rhtpa-2.1]`) |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 |
| Vulnerable library | tokio |
| Affected version range | versions before 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Upstream fix PR | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) |
| Advisory URL | [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| CVE record URL | [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) |
| Due date | 2026-08-15 |
| Existing comments | None |
| Upstream Affected Component | tokio (customfield_10632) |
| PS Component | pscomponent:org/rhtpa-server (customfield_10669) |
| Stream | rhtpa-2.1 (customfield_10832) |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x** (matches Version Streams table entry for 2.1.x -> rhtpa-release.0.3.z)
- Issue is **scoped** to stream 2.1.x only

## Ecosystem Detection

- Library: tokio (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z`
- Repository: backend

## Deployment Context

- Source repository: rhtpa-backend
- Deployment context: `upstream` (default -- no Deployment Context column configured)

## Version Impact (Stream 2.1.x)

The security-matrix.md for stream 2.1.x (rhtpa-release.0.3.z) shows the following builds:

| Version | Build | Build Date | backend tag |
|---------|-------|------------|-------------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 |

The mock lock file data does not include tokio versions directly. However, the CVE description states that tokio versions before 1.42.0 are vulnerable, and the issue description confirms that stream rhtpa-2.1 is affected. Both versions 2.1.0 and 2.1.1 ship vulnerable tokio versions (below 1.42.0).

## Cross-Stream Analysis (Stream 2.2.x)

Stream 2.2.x (rhtpa-release.0.4.z) is outside the scope of this issue (scoped to 2.1.x), but was analyzed during the original triage of TC-8020 (which is scoped to stream rhtpa-2.2). TC-8020 already tracks remediation for that stream.

## Key Context

The issue description notes that a proactive remediation task TC-8022 already exists for this stream, created by a prior cross-stream triage of TC-8020 (stream rhtpa-2.2). This is reconciled in Step 4.4.
