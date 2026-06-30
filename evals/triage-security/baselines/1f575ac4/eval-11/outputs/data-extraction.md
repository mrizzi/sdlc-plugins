# Step 1 -- Data Extraction for TC-8021

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
| Assignee | Unassigned |
| Status | New |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped to stream: **2.1.x** (Konflux release repo: `rhtpa-release.0.3.z`)
- This is a **stream-scoped** issue -- Steps 3-4 apply only to the 2.1.x stream

## Ecosystem Detection

- Vulnerable library: **tokio** (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z`

## Custom Fields

| Custom Field | Value |
|---|---|
| customfield_10632 (Upstream Affected Component) | tokio |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-server |
| customfield_10832 (Stream) | rhtpa-2.1 |

## Remote Links

| Title | URL | Type |
|-------|-----|------|
| GHSA-2026-tk91-v5pp | https://github.com/advisories/GHSA-2026-tk91-v5pp | GitHub Advisory |
| CVE-2026-55123 | https://www.cve.org/CVERecord?id=CVE-2026-55123 | CVE Record |
| tokio-rs/tokio#7001 | https://github.com/tokio-rs/tokio/pull/7001 | Upstream fix PR |

## Version Impact Table (from security-matrix.md mock data)

The mock data does not include tokio versions directly, but per the issue description, tokio versions before 1.42.0 are vulnerable. Since the issue is scoped to stream 2.1.x, only the 2.1.x stream versions are in scope for this issue:

| Version | Build Tag | Stream | Affected? | Notes |
|---------|-----------|--------|-----------|-------|
| 2.1.0 | v0.3.8 | 2.1.x | YES | tokio < 1.42.0 (per CVE data) |
| 2.1.1 | v0.3.12 | 2.1.x | YES | tokio < 1.42.0 (per CVE data) |

Cross-stream analysis (for Case B consideration):

| Version | Build Tag | Stream | Affected? | Notes |
|---------|-----------|--------|-----------|-------|
| 2.2.0 | v0.4.5 | 2.2.x | YES | tokio < 1.42.0 (per CVE data) |
| 2.2.1 | v0.4.8 | 2.2.x | YES | tokio < 1.42.0 (per CVE data) |
| 2.2.2 | v0.4.9 | 2.2.x | YES | retag of 2.2.1 |
| 2.2.3 | v0.4.11 | 2.2.x | Needs verification | |
| 2.2.4 | v0.4.12 | 2.2.x | Needs verification | |
