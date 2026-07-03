# Step 1 -- Data Extraction for TC-8003

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | (none found in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | (none) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. Mapping this to the
configured Version Streams in Security Configuration:

- Parsed suffix: `[rhtpa-2.2]` maps to stream **2.2.x**
- Matched Version Stream: **2.2.x** at `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Issue stream scope: **2.2.x only** (scoped issue -- Steps 3-4 apply only to this stream)

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The 2.2.x stream's
`security-matrix.md` Ecosystem Mappings table confirms:

- Ecosystem: **Cargo**
- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`

## Deployment Context Lookup

The affected component `pscomponent:org/rhtpa-server` maps to repository `rhtpa-backend`
in the Source Repositories table. No Deployment Context column is present in the
Source Repositories table, so the default deployment context is **upstream**.

## Configuration Extracted (Step 0)

| Config Field | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |

## Matrix Staleness Check (Step 0.3)

The security matrix has a `Last-Updated` timestamp of `2026-06-28T10:00:00Z`.
Current date is 2026-07-03. That is 5 days ago, which is within the 14-day
staleness threshold. Proceeding without a staleness warning.
