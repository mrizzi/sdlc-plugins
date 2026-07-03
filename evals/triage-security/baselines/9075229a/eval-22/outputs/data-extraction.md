# Step 1 -- Data Extraction: TC-8021

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches Component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | [rhtpa-2.2] | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | < 0.11.14 ("versions before 0.11.14") | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 (quinn-rs/quinn#2048) | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |
| Upstream Affected Component | quinn-proto | customfield_10632 |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`.

1. Parsed suffix: `rhtpa-2.2` maps to stream **2.2.x**.
2. Matched to Version Streams table: stream `2.2.x` is configured with Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.4.z`.
3. **Issue stream scope**: 2.2.x (scoped issue -- Steps 3-4 apply only to this stream for Affects Versions and duplicate detection).

The issue is **stream-scoped** to 2.2.x. While all streams are checked for version impact (Step 2), Affects Versions correction (Step 3) and remediation task creation (Step 8) are scoped to the 2.2.x stream only. Cross-stream impact on 2.1.x is handled via Case B.

## Ecosystem Detection

- **Library**: quinn-proto (Rust crate)
- **Detected ecosystem**: Cargo
- The 2.2.x stream's Ecosystem Mappings table includes Cargo with:
  - Repository: backend
  - Lock File: `Cargo.lock`
  - Check Command: `git show <tag>:Cargo.lock`
  - Upstream Branch: `release/0.4.z`
- Cargo is a source dependency ecosystem, so remediation produces **two tasks**: upstream backport + downstream propagation.

## Deployment Context Lookup

- Component label `pscomponent:org/rhtpa-server` maps to repository `rhtpa-backend`.
- Source Repositories table has `rhtpa-backend` at URL `https://github.com/rhtpa/rhtpa-backend`.
- No Deployment Context column is present in the Source Repositories table (backward compatibility).
- **Deployment context**: `upstream` (default).

## Version Impact Analysis (Step 2)

Using the mock lock file data from security-matrix-mock.md, the quinn-proto versions by pinned tag are:

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | quinn-proto Version | Affected? (< 0.11.14) |
|---------|-----------|--------------------|-----------------------|
| 2.1.0 | v0.3.8 | 0.11.9 | **YES** |
| 2.1.1 | v0.3.12 | 0.11.9 | **YES** |

### Stream 2.2.x (rhtpa-release.0.4.z) -- Issue Scoped Stream

| Version | Build Tag | quinn-proto Version | Affected? (< 0.11.14) |
|---------|-----------|--------------------|-----------------------|
| 2.2.0 | v0.4.5 | 0.11.9 | **YES** |
| 2.2.1 | v0.4.8 | 0.11.12 | **YES** |
| 2.2.2 | v0.4.9 | _(retag of v0.4.8)_ = 0.11.12 | **YES** (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.11.14 | **NO** (at fix version) |
| 2.2.4 | v0.4.12 | 0.11.14 | **NO** (at fix version) |

### Summary

- **Within scoped stream (2.2.x)**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 ship the fixed version (0.11.14) and are NOT affected.
- **Cross-stream (2.1.x)**: Both versions 2.1.0 and 2.1.1 are affected (ship 0.11.9). This triggers Case B cross-stream impact handling.

### Affects Versions Correction (Step 3)

- **Current Affects Versions**: RHTPA 2.0.0
- **PSIRT version is wrong**: There is no 2.0.x stream configured. RHTPA 2.0.0 does not correspond to any supported version.
- **Proposed Affects Versions** (scoped to 2.2.x stream): RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14 (the fixed version).
- The 2.1.x versions (2.1.0, 2.1.1) are NOT included in this issue's Affects Versions because the issue is scoped to stream 2.2.x. They would be tracked by a companion issue for stream 2.1.x.
