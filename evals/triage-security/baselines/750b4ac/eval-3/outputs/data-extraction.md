# Step 1 -- Data Extraction

## Issue Details

| Field | Value |
|-------|-------|
| Issue Key | TC-8003 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server |
| Affects Versions (PSIRT-claimed) | RHTPA 2.2.0 |
| Due Date | 2026-07-15 |
| Assignee | Unassigned |

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches `pscomponent:` pattern) |
| Vulnerable library | quinn-proto | Description |
| Affected version range | < 0.11.14 (versions before 0.11.14) | Description |
| Fixed version | 0.11.14 | Description |
| CVSS | 7.5 (High) | Description |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Upstream fix PR | None found | Remote links |
| Existing comments | None | Issue comments |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`.

1. Parsed suffix: `[rhtpa-2.2]` -> stream `2.2.x`
2. Matched to Version Streams table: `2.2.x` maps to Konflux release repo `rhtpa-release.0.4.z` at `/home/dev/repos/rhtpa-release.0.4.z`
3. Issue stream scope: **2.2.x only** (scoped issue -- Steps 2-7 apply only to this stream)

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md:

- **Ecosystem**: Cargo
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Source repository**: backend (upstream branch: `release/0.4.z`)

Cargo is a source dependency ecosystem, so remediation (if needed) would require two tasks: an upstream backport task and a downstream propagation subtask.
