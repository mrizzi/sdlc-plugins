# Step 1 -- Data Extraction for TC-8001

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | (none) |
| Reporter | psirt-analyst (account ID: 557058:psirt-analyst-mock-id) |

## Stream Scope Resolution

Issue summary suffix: `[rhtpa-2.2]` maps to configured Version Stream **2.2.x**.

This issue is **stream-scoped** to the 2.2.x stream. Steps 3 and 4 will apply only to versions within the 2.2.x stream.

## Ecosystem Detection

Vulnerable library: **quinn-proto** -- this is a Rust crate.
Ecosystem: **Cargo**
Lock file: `Cargo.lock`
Check command: `git show <tag>:Cargo.lock`

## Deployment Context Lookup

Affected repository: rhtpa-backend (matched from component label `pscomponent:org/rhtpa-server`)
Source Repositories table has no Deployment Context column -- defaulting to **upstream**.
