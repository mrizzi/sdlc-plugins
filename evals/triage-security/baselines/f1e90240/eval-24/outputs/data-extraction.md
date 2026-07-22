# Step 1 -- Data Extraction: TC-8001

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
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | (none) |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]` maps to stream **2.2.x**
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- The issue is **scoped** to the 2.2.x stream only

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Repository: backend
- Upstream branch (2.1.x): `release/0.3.z`
- Upstream branch (2.2.x): `release/0.4.z`

## Deployment Context

Source Repositories table does not have a Deployment Context column. Per backward compatibility rules, coordination guidance is omitted from remediation tasks.

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Build Tag | quinn-proto | Affected? | Notes |
|--------|---------|-----------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | fixed at 0.11.14 |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | fixed at 0.11.14 |

## Affects Versions Correction (Step 3)

- Current (PSIRT-assigned): `RHTPA 2.0.0` -- INCORRECT (version 2.0.0 does not exist in any stream)
- Issue is scoped to stream 2.2.x, so only 2.2.x versions are included
- Proposed: `RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2`
- Versions 2.2.3 and 2.2.4 are NOT affected (ship quinn-proto 0.11.14, which is the fixed version)

## Cross-Stream Impact (Step 8, Case B)

The issue is scoped to 2.2.x, but the 2.1.x stream is also affected:

| Stream | Versions Affected | quinn-proto versions |
|--------|-------------------|----------------------|
| 2.1.x | 2.1.0, 2.1.1 | 0.11.9 (both) |

Stream 2.1.x does not have its own CVE Jira for CVE-2026-31812 -- preemptive remediation tasks should be created.
