# Step 1 -- Data Extraction

## Issue: TC-8001

### Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`) and summary text |
| Affected component | `pscomponent:org/rhtpa-server` | Labels (matches `pscomponent:` pattern from Security Configuration) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | < 0.11.14 (versions before 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS score | 7.5 (High) | Description text |
| Vulnerability type | Denial of Service (DoS) | Description text (panic on large stream counts) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote links |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote links |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |
| Status | New | Issue status field |
| Assignee | Unassigned | Issue assignee field |

### Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`:

1. **Parsed suffix**: `[rhtpa-2.2]` maps to stream **2.2.x**
2. **Matched to Version Streams**: stream 2.2.x is configured at `git.example.com/rhtpa/rhtpa-release.0.4.z`
3. **Issue stream scope**: **2.2.x** (scoped issue)

This is a **scoped** issue -- Steps 3-4 will apply only to the 2.2.x stream for Affects Versions correction, while the version impact analysis (Step 2) still checks all streams to detect cross-stream impact (Case B).

### Ecosystem Detection

- **Vulnerable library**: quinn-proto
- **Detected ecosystem**: **Cargo** (Rust crate)
- **Rationale**: quinn-proto is a Rust crate (part of the quinn QUIC implementation). The Ecosystem Mappings table in the security matrix confirms Cargo is a configured ecosystem with lock file `Cargo.lock` and check command `git show <tag>:Cargo.lock`.
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Upstream branch (2.1.x stream)**: `release/0.3.z`
- **Upstream branch (2.2.x stream)**: `release/0.4.z`

### Deployment Context Lookup

- **Affected repository**: rhtpa-backend (resolved from component label `pscomponent:org/rhtpa-server`)
- **Source Repositories mapping**: rhtpa-backend found in Source Repositories table
- **Deployment context**: `upstream` (default -- no Deployment Context column in the Source Repositories table)

### Affects Versions Discrepancy (Preliminary)

The PSIRT-assigned Affects Version **RHTPA 2.0.0** appears incorrect:

- There is no 2.0.x stream configured in the Version Streams table
- The issue is scoped to the **2.2.x** stream per the `[rhtpa-2.2]` suffix
- This will be corrected in Step 3 after version impact analysis confirms which 2.2.x versions are actually affected

### Vulnerability Details

quinn-proto (before version 0.11.14) does not properly validate the number of streams requested in a QUIC STREAMS frame. An attacker can send a specially crafted frame that causes the server to allocate an unbounded number of stream state objects, leading to a panic when the allocation exceeds internal limits. This is classified as a Denial of Service (DoS) vulnerability.

### References

- Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq
- RustSec: https://rustsec.org/advisories/RUSTSEC-2026-0042.html
- Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
- CVE record: https://www.cve.org/CVERecord?id=CVE-2026-31812

### Version Data from Security Matrix (for Step 2)

The mock lock file data provides quinn-proto versions at each pinned tag:

| Tag | quinn-proto version | Affected? (< 0.11.14) |
|-----|---------------------|-----------------------|
| `v0.3.8` (2.1.0) | 0.11.9 | YES |
| `v0.3.12` (2.1.1) | 0.11.9 | YES |
| `v0.4.5` (2.2.0) | 0.11.9 | YES |
| `v0.4.8` (2.2.1) | 0.11.12 | YES |
| `v0.4.9` (2.2.2) | _(retag of v0.4.8)_ | YES (same as 2.2.1) |
| `v0.4.11` (2.2.3) | 0.11.14 | NO (fixed version) |
| `v0.4.12` (2.2.4) | 0.11.14 | NO (fixed version) |

### Preliminary Version Impact Summary

Based on the extracted data, the version impact table for Step 2 would show:

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

### Triage Path Preview

- **Issue scope**: 2.2.x stream only
- **Affected 2.2.x versions**: 2.2.0, 2.2.1, 2.2.2 (3 versions)
- **Not affected 2.2.x versions**: 2.2.3, 2.2.4 (ship fixed quinn-proto 0.11.14)
- **Cross-stream impact**: 2.1.x stream is also affected (all versions ship 0.11.9) -- this triggers Case B (cross-stream impact comment + proactive remediation if no sibling CVE Jira exists for 2.1.x)
- **Ecosystem**: Cargo -- remediation would create 2 tasks (upstream backport + downstream propagation) per affected stream
- **Affects Versions correction needed**: RHTPA 2.0.0 is incorrect; should be corrected to affected 2.2.x versions within scope
