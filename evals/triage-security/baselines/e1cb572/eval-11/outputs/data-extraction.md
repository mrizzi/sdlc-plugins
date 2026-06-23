# Step 1 -- Data Extraction

## Issue: TC-8021

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
| Upstream fix PR | tokio-rs/tokio#7001 (https://github.com/tokio-rs/tokio/pull/7001) |
| Advisory URL | GHSA-2026-tk91-v5pp (https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Due date | 2026-08-15 |
| Existing comments | None |
| Assignee | Unassigned |
| Status | New |

## Custom Fields

| Custom Field | Value |
|-------------|-------|
| customfield_10632 (Upstream Affected Component) | tokio |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-server |
| customfield_10832 (Stream) | rhtpa-2.1 |

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x** (matches Version Streams table row: 2.1.x at git.example.com/rhtpa/rhtpa-release.0.3.z)
- Issue is **stream-scoped** to 2.1.x only
- Konflux release repo local path: /home/dev/repos/rhtpa-release.0.3.z

## Ecosystem Detection

- Vulnerable library: **tokio** (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "tokio"'`
- Source repository: backend (from Ecosystem Mappings)
- Upstream branch: `release/0.3.z`

## Version Impact Analysis (Step 2)

Since the issue is scoped to stream 2.1.x, the primary analysis covers versions in that stream. The security matrix mock does not include explicit tokio version data in the lock file tables, but the issue description confirms tokio versions before 1.42.0 are vulnerable. In a real triage, `git show <tag>:Cargo.lock` would be run for each pinned tag to extract the tokio version.

Based on the issue description and Affects Versions field (RHTPA 2.1.0 and RHTPA 2.1.1), the PSIRT assessment indicates both 2.1.x versions are affected.

### Version Impact Table (stream 2.1.x)

| Version | Build Tag | tokio version | Affected? | Notes |
|---------|-----------|---------------|-----------|-------|
| 2.1.0 | v0.3.8 | < 1.42.0 (per PSIRT) | YES | Pinned in Cargo.lock |
| 2.1.1 | v0.3.12 | < 1.42.0 (per PSIRT) | YES | Pinned in Cargo.lock |

### Cross-stream Analysis (for Case B assessment)

The 2.2.x stream is also configured. Cross-stream impact was already assessed during prior triage of TC-8020 (stream rhtpa-2.2), which resulted in the creation of preemptive task TC-8022 for stream rhtpa-2.1.

| Version | Build Tag | tokio version | Affected? | Notes |
|---------|-----------|---------------|-----------|-------|
| 2.2.0 | v0.4.5 | assessed by TC-8020 | -- | Covered by TC-8020 |
| 2.2.1 | v0.4.8 | assessed by TC-8020 | -- | Covered by TC-8020 |
| 2.2.2 | v0.4.9 | assessed by TC-8020 | -- | Retag of 2.2.1 |
| 2.2.3 | v0.4.11 | assessed by TC-8020 | -- | Covered by TC-8020 |
| 2.2.4 | v0.4.12 | assessed by TC-8020 | -- | Covered by TC-8020 |
