# Step 1 — Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
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

## Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the configured **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x. Steps 3 and 4 will apply only to versions within the 2.2.x stream.

## Ecosystem Detection

Vulnerable library `quinn-proto` is a **Cargo** (Rust) crate. The 2.2.x stream's Ecosystem Mappings table confirms Cargo is a supported ecosystem:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

Investigation method: Lock file inspection via `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`.

## Deployment Context Lookup

The affected component label `pscomponent:org/rhtpa-server` maps to the **rhtpa-backend** source repository. Looking up the deployment context from the Source Repositories table in Security Configuration:

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | **customer-shipped** |

Deployment context for rhtpa-backend: **customer-shipped**

This deployment context will be used in Step 8 (Remediation) to generate coordination guidance in the remediation task descriptions.

## Version Impact Analysis (Step 2)

### Aggregated Supportability Matrix

**Stream 2.1.x** (rhtpa-release.0.3.z):

| Version | Build | Build Date | backend tag |
|---------|-------|------------|-------------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` |

**Stream 2.2.x** (rhtpa-release.0.4.z):

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

### Dependency Versions Extracted from Lock Files

quinn-proto versions by pinned backend tag (via `git show <tag>:Cargo.lock`):

| Tag | quinn-proto version |
|-----|---------------------|
| `v0.3.8` | 0.11.9 |
| `v0.3.12` | 0.11.9 |
| `v0.4.5` | 0.11.9 |
| `v0.4.8` | 0.11.12 |
| `v0.4.9` | _(retag of v0.4.8)_ |
| `v0.4.11` | 0.11.14 |
| `v0.4.12` | 0.11.14 |

### Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | **YES** | |
| 2.1.1 | 2.1.x | 0.11.9 | **YES** | |
| 2.2.0 | 2.2.x | 0.11.9 | **YES** | |
| 2.2.1 | 2.2.x | 0.11.12 | **YES** | |
| 2.2.2 | 2.2.x | — | **YES** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

### Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 | **NO** |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |

- **2.2.x (release/0.4.z)**: Fix is already present upstream. Remediation is a downstream propagation to ensure affected versions are superseded.
- **2.1.x (release/0.3.z)**: Fix is NOT present upstream. Remediation requires an upstream PR to bump quinn-proto to >= 0.11.14 on release/0.3.z, then downstream propagation.

### Affects Versions Correction (Step 3)

PSIRT-assigned Affects Versions `RHTPA 2.0.0` is incorrect — no 2.0.x stream exists.

Scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`:

- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14 (the fixed version).

### Cross-Stream Impact (Case B)

Stream 2.1.x is also affected (2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). This stream is outside the current issue's scope (`[rhtpa-2.2]`). Cross-stream impact will be reported and preemptive remediation tasks created for stream 2.1.x if no sibling CVE Jira exists for that stream.
