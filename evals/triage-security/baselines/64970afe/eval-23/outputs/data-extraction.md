# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | (none) |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`)
- Issue is **scoped** to the 2.2.x stream

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`

## Deployment Context Lookup

- Component label: `pscomponent:org/rhtpa-server`
- Matched Source Repository: **rhtpa-backend**
- Source Repositories table entry:

  | Repository | URL | Local Path | Deployment Context |
  |------------|-----|------------|--------------------|
  | rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | customer-shipped |

- Deployment context: **customer-shipped**

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto versions before 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | fixed at 0.11.14 |
| 2.2.4 | 2.2.x | 0.11.14 | NO | fixed at 0.11.14 |

### Affects Versions Correction

- **Current** (PSIRT-assigned): RHTPA 2.0.0
- **Corrected** (based on lock file evidence): RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- RHTPA 2.0.0 is incorrect -- there is no 2.0.x version stream in the configuration. PSIRT likely assigned this based on scan time rather than actual dependency analysis.
- Versions 2.2.3 and 2.2.4 are NOT affected (ship quinn-proto 0.11.14, which is the fixed version).

### Cross-Stream Impact

The issue is scoped to 2.2.x, but the 2.1.x stream is also affected:
- 2.1.0 ships quinn-proto 0.11.9 (affected)
- 2.1.1 ships quinn-proto 0.11.9 (affected)

This triggers Case B (cross-stream impact -- proactive remediation for 2.1.x).
