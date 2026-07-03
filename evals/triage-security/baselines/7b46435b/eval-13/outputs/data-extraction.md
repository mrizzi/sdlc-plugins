# Step 1 -- Data Extraction for TC-8001

## Parsed CVE Data

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
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Ecosystem | Cargo (Rust crate) |
| Lock file | Cargo.lock |
| Check command | `git show <tag>:Cargo.lock \| grep -A2 'name = "quinn-proto"'` |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo `rhtpa-release.0.4.z`). This issue is **stream-scoped** to 2.2.x. Steps 3 and 8 apply only to the 2.2.x stream; cross-stream impact on 2.1.x is handled via Case B.

## Deployment Context

The affected repository `rhtpa-backend` has deployment context **upstream** (default, since no Deployment Context column is present in the Source Repositories table).

## Affects Versions Mismatch (Preliminary)

The PSIRT-assigned Affects Version `RHTPA 2.0.0` does not correspond to any version in the configured version streams (2.1.x or 2.2.x). This will be corrected in Step 3 after version impact analysis confirms which versions are actually affected.
