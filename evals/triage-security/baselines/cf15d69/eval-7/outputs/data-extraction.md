# Step 1 -- Data Extraction: TC-8006

## Extracted Fields

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Affects Versions (Jira field) | RHTPA 2.1.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | (none found in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | (none) |
| Assignee | Unassigned |
| Status | New |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x** (matches Version Streams row: 2.1.x -> rhtpa-release.0.3.z at /home/dev/repos/rhtpa-release.0.3.z)
- Issue is **scoped** to stream 2.1.x only

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Repository: backend
- Upstream branch: `release/0.3.z` (for stream 2.1.x)

## Existing Issue Links

- **Related**: TC-8001 (CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2])
  - Link ID: 1990401
  - Type: Related
  - Direction: outward (TC-8006 -> TC-8001)

## Remote Links

- GHSA-2026-qp73-x4mq (GitHub Advisory)
- CVE-2026-31812 (CVE Record)

## Step 1.5 -- External CVE Data Enrichment

### MITRE CVE API

Query: `https://cveawg.mitre.org/api/cve/CVE-2026-31812`

Expected structured data:
- Product: quinn-proto
- Affected: versions lessThan 0.11.14
- Fixed version: 0.11.14

### OSV.dev API

Query: `https://api.osv.dev/v1/vulns/CVE-2026-31812`

Expected structured data:
- Package: quinn-proto
- Ecosystem: crates.io
- Introduced: 0 (all versions before fix)
- Fixed: 0.11.14

### Cross-validation

| Source | Affected range | Fixed version |
|--------|---------------|---------------|
| Jira description | < 0.11.14 | 0.11.14 |
| MITRE CVE API | < 0.11.14 | 0.11.14 |
| OSV.dev | < 0.11.14 | 0.11.14 |

All sources agree. Enriched fix threshold: **0.11.14**

## Version Impact Analysis (Step 2)

Using mock lock file data from security-matrix-mock.md for the 2.1.x stream (scoped):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | 0.11.9 | YES | 0.11.9 < 0.11.14 |

Both versions in the 2.1.x stream ship quinn-proto 0.11.9, which is below the fix threshold of 0.11.14.

### Cross-stream impact (all streams, for Case B analysis)

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | Fixed at threshold |
| 2.2.4 | 2.2.x | 0.11.14 | NO | Fixed at threshold |

Stream 2.2.x is also partially affected (versions 2.2.0-2.2.2), but that stream is tracked by sibling TC-8001.
