# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to configured Version Stream **2.2.x** (Konflux release repo `rhtpa-release.0.4.z`). This issue is **scoped** to stream 2.2.x only.

## Ecosystem Detection

- **Ecosystem**: Cargo (Rust crate)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Upstream branch (2.1.x)**: `release/0.3.z`
- **Upstream branch (2.2.x)**: `release/0.4.z`

## Deployment Context Lookup

- **Affected repository**: rhtpa-backend (matched from component label `pscomponent:org/rhtpa-server`)
- **Source Repositories table entry**: rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | **customer-shipped**
- **Deployment context**: **customer-shipped**

This deployment context will be used in Step 8 (Remediation) to generate coordination guidance in remediation task descriptions. Per the `customer-shipped` context, remediation tasks will include guidance to coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure.

## Version Impact Analysis (Step 2)

### Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | fixed version shipped |
| 2.2.4 | 2.2.x | 0.11.14 | NO | fixed version shipped |

### Affects Versions Correction (Step 3)

PSIRT assigned `RHTPA 2.0.0`, which does not match any supported version. The correct Affects Versions, scoped to stream 2.2.x per the issue suffix, are:

- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are NOT affected (they ship quinn-proto 0.11.14, which is the fixed version).

### Cross-Stream Impact (Case B)

Stream 2.1.x is also affected (both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9, which is below the fix threshold of 0.11.14). Since TC-8001 is scoped to stream 2.2.x, the 2.1.x impact is reported as cross-stream and would trigger Case B preemptive remediation if no companion CVE Jira exists for 2.1.x.
