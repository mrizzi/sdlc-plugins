# Step 1 - Data Extraction for TC-8003

## Validated Configuration (Step 0)

| Config Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend) |

## Extracted CVE Data

| Field | Value |
|---|---|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] (stream suffix) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Assignee | Unassigned |
| Status | New |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. This maps to the **2.2.x** version stream in the Security Configuration, served by the Konflux release repo `rhtpa-release.0.4.z`.

This issue is **stream-scoped** to the 2.2.x stream. Steps 3 and 4 will be scoped to versions within this stream only.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, this falls under the **Cargo** ecosystem:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| Cargo | backend | Cargo.lock | `git show <tag>:Cargo.lock` | release/0.4.z |

Investigation method: Lock file inspection via `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`

## Version Impact Analysis (Step 2)

### Scoped stream: 2.2.x

Using the supportability matrix for Stream 2 (rhtpa-release.0.4.z):

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---|---|---|---|---|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Cross-stream analysis: 2.1.x

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---|---|---|---|---|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD (latest tag) | Fixed? |
|---|---|---|---|---|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (at v0.4.11+) | YES |

The upstream fix is already present on the release/0.4.z branch (quinn-proto 0.11.14 shipped since build v0.4.11 / version 2.2.3).

### Conclusion

Within the scoped 2.2.x stream, versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fixed version (0.11.14). The vulnerability was remediated in the 2.2.x stream starting with build v0.4.11.
