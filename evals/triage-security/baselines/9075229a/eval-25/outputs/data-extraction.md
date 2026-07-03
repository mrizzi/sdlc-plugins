# Step 1 -- Data Extraction: TC-8040

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table. This issue is **stream-scoped** to stream 2.2.x only.

## Ecosystem Detection

The vulnerable library is **quinn-proto**. Based on contextual analysis, the detected ecosystem is **Go modules**.

The Ecosystem Mappings tables for both configured streams (2.1.x and 2.2.x) list only the following supported ecosystems:

- **Cargo** -- Rust crates
- **RPM** -- System packages

**Go modules** is not listed in any stream's Ecosystem Mappings table. Automated triage cannot proceed for this ecosystem.

## Deployment Context Lookup

The affected component label `pscomponent:org/rhtpa-server` does not directly match any entry in the Source Repositories table (which lists `rhtpa-backend`). Per skill rules, defaulting deployment context to **upstream**.

The Source Repositories table has no Deployment Context column, so all repositories default to `upstream` per backward compatibility rules.
