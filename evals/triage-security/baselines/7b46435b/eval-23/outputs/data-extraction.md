# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Mapped repository | rhtpa-backend |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x (scoped to rhtpa-release.0.4.z) |
| Affects Versions (Jira field) | RHTPA 2.0.0 (incorrect -- no such version exists) |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Ecosystem | Cargo |
| Due date | 2026-07-15 |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Additional reference | [RUSTSEC-2026-0042](https://rustsec.org/advisories/RUSTSEC-2026-0042.html) |

## Deployment Context Lookup

The affected repository `rhtpa-backend` was looked up in the Source Repositories
table from the project's CLAUDE.md Security Configuration:

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | **customer-shipped** |

**Result:** Deployment context is `customer-shipped`. This means coordination
with Product Security is required for CVE assignment, advisory preparation, and
formal disclosure. The fix must be released via a security advisory with explicit
CVE-to-component mapping.

## Version Impact Analysis

### Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Build | Backend Tag | quinn-proto | Affected? | Notes |
|--------|---------|-------|-------------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | 0.3.8 | `v0.3.8` | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | 0.3.12 | `v0.3.12` | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | 0.4.5 | `v0.4.5` | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | 0.4.8 | `v0.4.8` | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | 0.4.9 | `v0.4.8` | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | 0.4.11 | `v0.4.11` | 0.11.14 | NO | ships fixed version |
| 2.2.x | 2.2.4 | 0.4.12 | `v0.4.12` | 0.11.14 | NO | ships fixed version |

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (at v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (at v0.4.12) | YES |

### Stream Scope Analysis

This issue is scoped to stream **2.2.x** (per summary suffix `[rhtpa-2.2]`).

**2.2.x stream (scoped):**
- Affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- Already fixed in: RHTPA 2.2.3, RHTPA 2.2.4 (quinn-proto 0.11.14)
- Upstream branch release/0.4.z: already ships fixed version
- **No remediation task needed** -- fix is already present in the latest releases

**2.1.x stream (cross-stream impact):**
- All versions affected: RHTPA 2.1.0, RHTPA 2.1.1 (quinn-proto 0.11.9)
- Upstream branch release/0.3.z: still ships vulnerable version (0.11.9)
- **Remediation needed** -- upstream backport required

### Affects Versions Correction

Current (PSIRT-assigned): `[RHTPA 2.0.0]`
Proposed (scoped to 2.2.x stream): `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Rationale: RHTPA 2.0.0 does not correspond to any version in the supportability
matrix. Lock file analysis at pinned commits shows versions 2.2.0 through 2.2.2
ship quinn-proto < 0.11.14 (the vulnerable range). Versions 2.2.3 and 2.2.4
already ship the fixed version 0.11.14.
