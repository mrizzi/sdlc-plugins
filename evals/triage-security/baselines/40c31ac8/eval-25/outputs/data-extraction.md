# Step 1 -- Data Extraction: TC-8040

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | `pscomponent:org/rhtpa-server` | Labels (matches component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Due date | 2026-07-15 | Jira `duedate` field |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote links |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote links |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote links |
| Existing comments | None | Issue comment history |
| Assignee | Unassigned | Jira `assignee` field |
| Status | New | Jira `status` field |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`.

- Parsed suffix: `rhtpa-2.2` maps to stream **2.2.x**
- Matched to Version Streams table: stream **2.2.x** at `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Issue stream scope: **2.2.x** (scoped to single stream)

## Ecosystem Detection

The vulnerable library `quinn-proto` was analyzed in the context of the component `pscomponent:org/rhtpa-server`.

- **Detected ecosystem: Go modules**

### Ecosystem Mappings Check

The Ecosystem Mappings table for the 2.2.x stream (`rhtpa-release.0.4.z`) lists the following supported ecosystems:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

**Result: "Go modules" is NOT listed in the Ecosystem Mappings table.**

The detected ecosystem does not match any configured ecosystem in either the 2.1.x or 2.2.x stream matrices. Both streams only support Cargo and RPM ecosystems. Automated triage cannot proceed for this ecosystem.

## Configuration Context (from CLAUDE.md)

| Setting | Value |
|---------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | pscomponent: |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| VEX Justification custom field | customfield_12345 |

## Affects Versions Mismatch (Preliminary)

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, but there is no 2.0.x stream configured in the Version Streams table. The issue is scoped to stream 2.2.x based on the summary suffix. This mismatch would normally be corrected in Step 3, but triage is halted before reaching that step due to the unsupported ecosystem.
