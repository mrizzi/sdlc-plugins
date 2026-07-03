# Step 1 -- Data Extraction

## Issue: TC-8001

Parsed CVE data from Vulnerability issue TC-8001:

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches Component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | < 0.11.14 (versions before 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote links |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote links |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote links |
| Due date | 2026-07-15 | Jira `duedate` field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`.

1. Parsed suffix: `rhtpa-2.2` maps to stream `2.2.x`
2. Matched to Version Streams table: stream **2.2.x** at `git.example.com/rhtpa/rhtpa-release.0.4.z`
3. Issue stream scope recorded: **2.2.x** (scoped -- Steps 3-4 will apply to this single stream only)

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Detected ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch (2.2.x stream): `release/0.4.z`

The Cargo ecosystem is listed in the stream's Ecosystem Mappings table. Automated triage proceeds.

## Deployment Context Lookup

- Affected repository (from component label `pscomponent:org/rhtpa-server`): rhtpa-backend
- Source Repositories match: rhtpa-backend at https://github.com/rhtpa/rhtpa-backend
- Deployment context: **upstream** (default -- no Deployment Context column in Source Repositories table)

## Observations

- The PSIRT-assigned Affects Versions field (`RHTPA 2.0.0`) does not correspond to any configured version stream (2.1.x or 2.2.x). This mismatch will be corrected in Step 3 based on lock file evidence from Step 2.
- The issue is stream-scoped to 2.2.x, so primary triage focuses on that stream. Cross-stream impact on 2.1.x will be evaluated in Step 2 and reported in Case B if applicable.
