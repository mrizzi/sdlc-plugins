# Step 1 -- Data Extraction

## Issue: TC-8001

### Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 (versions before 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Status | New |
| Existing comments | None |

### Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |

### Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the
**2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x. Steps 3-4 will apply only to
this stream's versions.

### Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Based on the Ecosystem
Mappings table in `security-matrix.md`, the ecosystem is **Cargo**.

- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Source repository**: backend
- **Upstream branch**: `release/0.4.z` (for the 2.2.x stream)

### Deployment Context

The affected component `pscomponent:org/rhtpa-server` maps to the
`rhtpa-backend` source repository. Per the Source Repositories table in
Security Configuration, the deployment context defaults to `upstream`
(no explicit Deployment Context column is present).

### Affects Versions Mismatch (Preliminary)

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, but no 2.0.x stream
is configured in the Version Streams table. The issue summary scopes it to
stream 2.2.x. This mismatch will be corrected in Step 3 after the version
impact analysis (Step 2) determines the actual affected versions based on
lock file evidence.

### quinn-proto Versions by Release (from security-matrix.md mock data)

| Product Version | Build Tag | quinn-proto Version | Affected? |
|-----------------|-----------|---------------------|-----------|
| 2.1.0 | v0.3.8 | 0.11.9 | Yes (< 0.11.14) |
| 2.1.1 | v0.3.12 | 0.11.9 | Yes (< 0.11.14) |
| 2.2.0 | v0.4.5 | 0.11.9 | Yes (< 0.11.14) |
| 2.2.1 | v0.4.8 | 0.11.12 | Yes (< 0.11.14) |
| 2.2.2 | v0.4.9 | (retag of v0.4.8 = 0.11.12) | Yes (< 0.11.14) |
| 2.2.3 | v0.4.11 | 0.11.14 | No (>= 0.11.14, fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | No (>= 0.11.14, fixed) |
