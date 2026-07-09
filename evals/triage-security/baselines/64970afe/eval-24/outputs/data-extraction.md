# Step 0 -- Configuration Validation

| Parameter | Value |
|-----------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Embargo policy URL | _(not configured -- Step 1.7 skipped)_ |
| Upstream Affected Component field | _(not configured -- Step 4.3 and Step 7 skipped)_ |
| ProdSec contact email | _(not configured)_ |
| ProdSec Jira account ID | _(not configured)_ |

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | _(column absent -- defaults to upstream; coordination guidance omitted)_ |

## Step 0.3 -- Matrix Staleness Check

Matrix `Last-Updated` timestamp: `2026-06-28T10:00:00Z` (11 days ago as of 2026-07-09).
This is within the 14-day freshness threshold. Proceeding without warning.

---

# Step 1 -- Data Extraction

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
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | _(none)_ |

### Stream Scope Resolution

Summary suffix `[rhtpa-2.2]` maps to stream **2.2.x**, which matches the Version Streams table.
This issue is **scoped** to the 2.2.x stream.

### Ecosystem Detection

Library `quinn-proto` is a Rust crate. Ecosystem: **Cargo**.
Both streams have Cargo configured in their Ecosystem Mappings tables:

| Stream | Repository | Lock File | Check Command | Upstream Branch |
|--------|------------|-----------|---------------|-----------------|
| 2.1.x | backend | Cargo.lock | `git show <tag>:Cargo.lock` | release/0.3.z |
| 2.2.x | backend | Cargo.lock | `git show <tag>:Cargo.lock` | release/0.4.z |

### Deployment Context

The Source Repositories table does not have a Deployment Context column.
Per backward compatibility rules, all repositories default to `upstream`.
Coordination guidance subsection will be omitted from remediation task descriptions.

---

# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrices

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction

Lock file inspection results (`git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`):

| Tag | quinn-proto version | Affected? |
|-----|---------------------|-----------|
| `v0.3.8` | 0.11.9 | YES (< 0.11.14) |
| `v0.3.12` | 0.11.9 | YES (< 0.11.14) |
| `v0.4.5` | 0.11.9 | YES (< 0.11.14) |
| `v0.4.8` | 0.11.12 | YES (< 0.11.14) |
| `v0.4.9` | _(retag of v0.4.8)_ | YES (same as v0.4.8) |
| `v0.4.11` | 0.11.14 | NO (= 0.11.14, fixed) |
| `v0.4.12` | 0.11.14 | NO (= 0.11.14, fixed) |

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | fixed version |

### Dependency Chain (Step 2.3.5)

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (Cargo)
  Profile: production (quinn-proto is a runtime QUIC protocol dependency)
```

## 2.5 -- Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.12) | YES |

- **2.2.x**: Fix already present since version 2.2.3 (tag v0.4.11). No new upstream backport needed.
- **2.1.x**: Fix NOT present. Upstream backport to release/0.3.z branch is required.

---

# Step 3 -- Affects Versions Correction

**PSIRT-assigned Affects Versions**: RHTPA 2.0.0

This is incorrect. RHTPA 2.0.0 does not correspond to any version in the configured
version streams (2.1.x or 2.2.x).

**Corrected Affects Versions** (based on lock file evidence, scoped to 2.2.x stream):
- RHTPA 2.2.0
- RHTPA 2.2.1
- RHTPA 2.2.2

Versions RHTPA 2.2.3 and RHTPA 2.2.4 are NOT affected (ship quinn-proto 0.11.14).

**Cross-stream impact** (2.1.x, outside issue scope):
- RHTPA 2.1.0 and RHTPA 2.1.1 are also affected but tracked separately (Case B).

---

# Triage Outcome Summary

- **Issue scope**: 2.2.x stream (from summary suffix `[rhtpa-2.2]`)
- **In-scope assessment**: Versions 2.2.0-2.2.2 are affected but the fix already landed in 2.2.3+. No remediation tasks needed for 2.2.x.
- **Cross-stream assessment (Case B)**: Stream 2.1.x is fully affected (all versions ship quinn-proto 0.11.9). Preemptive remediation tasks are needed for the 2.1.x stream since no stream-specific CVE Jira exists for 2.1.x.
- **Affects Versions correction**: Remove RHTPA 2.0.0, add RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2.
