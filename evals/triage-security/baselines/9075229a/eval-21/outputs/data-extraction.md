# Step 1 -- Data Extraction for TC-8020

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (component label pattern: `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote links |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote links |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |
| Upstream Affected Component | quinn-proto | customfield_10632 |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. Mapping this to the configured Version Streams:

- `[rhtpa-2.2]` maps to stream **2.2.x**
- This matches the Version Streams table entry: `2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z`
- **Issue stream scope**: 2.2.x (scoped to this single stream)

Steps 3-8 will be scoped to the 2.2.x stream only. Cross-stream impact on 2.1.x will be handled via Case B (cross-stream impact comment).

## Ecosystem Detection

- **Library**: quinn-proto (a Rust crate)
- **Detected ecosystem**: Cargo
- **Validation**: Cargo is listed in the 2.2.x stream's Ecosystem Mappings table
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Upstream branch**: `release/0.4.z`

Since the ecosystem is Cargo (a source dependency), remediation would require two tasks: an upstream backport task (fix in the source repo) and a downstream propagation subtask (update the reference in the Konflux release repo).

## Deployment Context Lookup

- Component label `pscomponent:org/rhtpa-server` maps to repository `rhtpa-backend`
- Source Repositories table entry: `rhtpa-backend | https://github.com/rhtpa/rhtpa-backend`
- Deployment Context column is absent in the mock configuration
- **Deployment context**: upstream (default when column is absent)

## Version Impact Analysis (Step 2)

Using lock file data from the security matrix for the scoped 2.2.x stream:

### 2.2.x Stream (scoped -- primary analysis)

| Version | Build Tag | quinn-proto Version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 (fix threshold) |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 (fix threshold) |
| 2.2.2 | v0.4.9 | 0.11.12 | YES | Retag of v0.4.8 -- same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (at fix threshold) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (at fix threshold) |

### 2.1.x Stream (out of scope -- cross-stream reference)

| Version | Build Tag | quinn-proto Version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 (fix threshold) |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 (fix threshold) |

## Affects Versions Assessment

- **Current (PSIRT-assigned)**: RHTPA 2.0.0
- **Correct (based on lock file analysis, scoped to 2.2.x)**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Not affected in 2.2.x stream**: RHTPA 2.2.3, RHTPA 2.2.4 (ship quinn-proto 0.11.14, at fix threshold)
- **Assessment**: PSIRT Affects Versions are incorrect. RHTPA 2.0.0 does not correspond to any configured stream version. Correction needed.

## Matrix Staleness Check (Step 0.3)

- Matrix Last-Updated: 2026-06-28T10:00:00Z
- Current date: 2026-07-03
- Days since update: 5 days
- Staleness threshold: 14 days
- **Result**: Matrix is fresh (5 days < 14-day threshold). Proceeding without staleness warning.
