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

Issue summary suffix `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`).

This issue is **scoped** to the 2.2.x stream. Steps 3-4 apply only to 2.2.x versions, but the full version impact analysis covers all configured streams (2.1.x and 2.2.x) for cross-stream impact detection (Case B).

## Ecosystem Detection

Library `quinn-proto` is a Rust crate. Ecosystem: **Cargo**.

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- Upstream branches: `release/0.3.z` (2.1.x), `release/0.4.z` (2.2.x)

## Deployment Context Lookup

Affected component `pscomponent:org/rhtpa-server` maps to source repository **rhtpa-backend**.

Source Repositories table entry:

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | customer-shipped |

Deployment context: **customer-shipped**

This deployment context will be used in Step 8 (Remediation) to generate coordination guidance in remediation task descriptions. Because this component is customer-shipped, remediation tasks must include guidance to coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure.

## Version Impact Analysis (Step 2)

### Aggregated Supportability Matrix

**Stream 2.1.x** (rhtpa-release.0.3.z):

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

**Stream 2.2.x** (rhtpa-release.0.4.z):

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

### Dependency Version Extraction (Step 2.3)

quinn-proto versions extracted from Cargo.lock at each pinned tag:

| Tag | quinn-proto version | Source |
|-----|---------------------|--------|
| `v0.3.8` | 0.11.9 | Cargo.lock |
| `v0.3.12` | 0.11.9 | Cargo.lock |
| `v0.4.5` | 0.11.9 | Cargo.lock |
| `v0.4.8` | 0.11.12 | Cargo.lock |
| `v0.4.9` | _(retag of v0.4.8)_ | same as v0.4.8 |
| `v0.4.11` | 0.11.14 | Cargo.lock |
| `v0.4.12` | 0.11.14 | Cargo.lock |

### Version Impact Table (Step 2.4)

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | fixed |
| 2.2.4 | 2.2.x | 0.11.14 | NO | fixed |

### Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at Latest Tag | Fixed? |
|--------|-----------|-----------------|----------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.11+) | YES |

- **2.2.x**: The upstream fix is already present. Versions 2.2.3+ ship quinn-proto 0.11.14. Remediation for this stream is a downstream propagation to ensure the Konflux release repo references reflect the fix.
- **2.1.x**: The upstream fix is NOT present on release/0.3.z. Remediation requires an upstream backport first, then downstream propagation.

### Affects Versions Correction (Step 3)

- **Current (PSIRT-assigned)**: RHTPA 2.0.0
- **Proposed (scoped to 2.2.x stream)**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

The PSIRT-assigned version "RHTPA 2.0.0" does not match any version in the supportability matrix. Based on lock file evidence, the affected versions in the 2.2.x stream are 2.2.0, 2.2.1, and 2.2.2 (quinn-proto < 0.11.14). Versions 2.2.3 and 2.2.4 ship the fixed version (0.11.14) and are NOT affected.

### Cross-Stream Impact (Case B)

This issue is scoped to 2.2.x, but the version impact analysis reveals that **stream 2.1.x is also affected**:

- 2.1.0: quinn-proto 0.11.9 (AFFECTED)
- 2.1.1: quinn-proto 0.11.9 (AFFECTED)

Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. This stream may require separate PSIRT triage or preemptive remediation tasks.
