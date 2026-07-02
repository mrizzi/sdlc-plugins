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
| Existing comments | (none) |
| Ecosystem | Cargo |
| Lock file | Cargo.lock |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo `rhtpa-release.0.4.z`). This issue is **stream-scoped** to 2.2.x only. Steps 3 and 4 apply to the 2.2.x stream; cross-stream impact on 2.1.x is handled via Case B (proactive remediation).

## Deployment Context Lookup

The affected component label `pscomponent:org/rhtpa-server` maps to the source repository **rhtpa-backend**. Looking up rhtpa-backend in the Source Repositories table from CLAUDE.md Security Configuration:

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | **customer-shipped** |

Deployment context for this CVE triage: **customer-shipped**

This means coordination with Product Security is required for CVE assignment, advisory preparation, and formal disclosure.

## Version Impact Table

Version impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | (cross-stream -- 2.1.x) |
| 2.1.1 | 0.11.9 | YES | (cross-stream -- 2.1.x) |
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 0.11.14 | NO | fixed at >= 0.11.14 |
| 2.2.4 | 0.11.14 | NO | fixed at >= 0.11.14 |

### In-scope affected versions (2.2.x stream)

Versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto < 0.11.14 and are affected.

### Cross-stream affected versions (2.1.x stream)

Versions 2.1.0 and 2.1.1 ship quinn-proto 0.11.9 (< 0.11.14) and are also affected. These are outside the issue's stream scope and will be handled via Case B proactive remediation.

### Affects Versions Correction

The current Affects Versions field is set to **RHTPA 2.0.0**, which does not correspond to any version in the supported version streams. Based on lock file evidence, the correct Affects Versions for this stream-scoped issue (2.2.x) should be:

- **RHTPA 2.2.0** (quinn-proto 0.11.9 -- affected)
- **RHTPA 2.2.1** (quinn-proto 0.11.12 -- affected)
- **RHTPA 2.2.2** (retag of 2.2.1 -- affected)

RHTPA 2.0.0 should be removed (no such version exists in the supportability matrix).

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Check Command | Notes |
|--------|-----------|-----------------|---------------|-------|
| 2.2.x | Cargo | release/0.4.z | `git show release/0.4.z:Cargo.lock` | v0.4.11+ already ships 0.11.14 -- fix is on this branch |
| 2.1.x | Cargo | release/0.3.z | `git show release/0.3.z:Cargo.lock` | v0.3.12 ships 0.11.9 -- needs upstream backport |
