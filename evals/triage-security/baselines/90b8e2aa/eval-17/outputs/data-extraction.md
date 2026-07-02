# Step 1 -- Data Extraction

## Parsed CVE Data for TC-8001

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x. Steps 3 and 4 will apply only to versions within the 2.2.x stream.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. The ecosystem is **Cargo**.

From the 2.2.x stream's Ecosystem Mappings:
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`
- Repository: backend

## Deployment Context

The affected repository (rhtpa-backend) has deployment context: **upstream** (default, as no Deployment Context column is present in the Source Repositories table).

## Affects Versions Discrepancy (Preliminary)

PSIRT assigned Affects Versions: **RHTPA 2.0.0**

There is no 2.0.x version stream configured. The issue summary suffix `[rhtpa-2.2]` indicates this should be scoped to the 2.2.x stream. The Affects Versions will need correction in Step 3 based on version impact analysis.
