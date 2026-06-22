# Step 1 -- Data Extraction: TC-8006

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Affects Versions (Jira field) | RHTPA 2.1.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | (none linked) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Status | New |
| Assignee | Unassigned |
| Existing comments | (none) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.1]`.

1. Parsed suffix: `rhtpa-2.1` maps to stream `2.1.x`
2. Matched to Version Streams table: stream `2.1.x` corresponds to Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.3.z` at local path `/home/dev/repos/rhtpa-release.0.3.z`
3. Issue stream scope: **2.1.x** (scoped issue -- Steps 2-7 apply only to this stream)

## Ecosystem Detection

The vulnerable library is `quinn-proto`, a Rust crate. From the security-matrix.md Ecosystem Mappings for the 2.1.x stream:

- Ecosystem: **Cargo**
- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.3.z`

## Existing Issue Links

The issue already has the following links:

- **Related** (outward): TC-8001 -- CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] (Link ID: 1990401)

## Remote Links

- GHSA-2026-qp73-x4mq (GitHub Advisory)
- CVE-2026-31812 (CVE Record)

## Version Impact Table (from mock lock file data)

For the 2.1.x stream (this issue's scope):

| Version | Tag | quinn-proto version | Affected? | Notes |
|---------|-----|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 |

Cross-stream reference (2.2.x stream, tracked by sibling TC-8001):

| Version | Tag | quinn-proto version | Affected? | Notes |
|---------|-----|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | v0.4.9 | (retag of v0.4.8) | YES | same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | fixed version |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | fixed version |

Both versions in the 2.1.x stream ship quinn-proto 0.11.9, which is within the vulnerable range (before 0.11.14). All 2.1.x versions are affected.
