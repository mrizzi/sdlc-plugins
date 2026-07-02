# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | (none) |

## Stream Scope

Issue summary contains `[rhtpa-2.2]` which maps to stream **2.2.x**. This is a **scoped** issue -- Steps 3-4 apply only to the 2.2.x stream. Cross-stream impact on other streams is handled via Case B.

## Ecosystem Detection

- **Ecosystem**: Cargo (Rust crate)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Repository**: backend
- **Upstream branch (2.1.x)**: `release/0.3.z`
- **Upstream branch (2.2.x)**: `release/0.4.z`

## Deployment Context

Source Repositories table does not include a Deployment Context column. Per backward compatibility rules, all repositories default to `upstream`. Coordination Guidance subsection is omitted from remediation task descriptions.

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | fixed version |

## Affects Versions Correction

- **Current (PSIRT-assigned)**: RHTPA 2.0.0
- **Corrected (scoped to 2.2.x)**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Rationale**: RHTPA 2.0.0 does not correspond to any configured version stream. Lock file analysis shows versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto < 0.11.14. Versions 2.2.3+ ship the fixed version 0.11.14.

## Cross-Stream Impact

Stream 2.1.x is also affected (versions 2.1.0 and 2.1.1 ship quinn-proto 0.11.9). This is outside the issue's scope ([rhtpa-2.2]) and triggers Case B (preemptive remediation).
