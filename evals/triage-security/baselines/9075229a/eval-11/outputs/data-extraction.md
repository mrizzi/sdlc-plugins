# Step 1 -- Data Extraction: TC-8021

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-55123 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Label matching `pscomponent:` pattern |
| Product version (PSIRT-claimed) | rhtpa-2.1 | Summary suffix `[rhtpa-2.1]` |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 | Jira `versions` field |
| Vulnerable library | tokio | Description text |
| Affected version range | versions before 1.42.0 | Description text |
| Fixed version | 1.42.0 | Description text |
| CVSS | 8.1 (High) | Description text |
| Upstream fix PR | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) | Remote links |
| Advisory URL | [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) | Remote links |
| CVE record URL | [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) | Remote links |
| Due date | 2026-08-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |

## Custom Fields

| Custom Field | Field ID | Value |
|-------------|----------|-------|
| Upstream Affected Component | customfield_10632 | tokio |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-server |
| Stream | customfield_10832 | rhtpa-2.1 |

## Stream Scope Resolution

- Issue summary suffix: `[rhtpa-2.1]`
- Parsed stream identifier: `2.1.x`
- Matched Version Stream: **2.1.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.3.z`)
- Issue stream scope: **scoped to 2.1.x only**

The suffix `[rhtpa-2.1]` maps to the configured `2.1.x` Version Stream. Steps 2-8 are scoped to this single stream.

## Ecosystem Detection

- Library: tokio (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z`

The tokio crate is a Rust dependency, matching the Cargo ecosystem in the 2.1.x stream's Ecosystem Mappings table. As a source dependency, remediation follows the two-task pattern (upstream backport + downstream propagation).

## Deployment Context Lookup

- Affected repository (from component label): rhtpa-backend
- Source Repositories match: rhtpa-backend (URL: https://github.com/rhtpa/rhtpa-backend)
- Deployment context: `upstream` (default -- no Deployment Context column in Source Repositories table)

## Issue Links

No existing issue links on TC-8021.
