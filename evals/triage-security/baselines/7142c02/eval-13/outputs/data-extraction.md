# Step 1 -- Data Extraction for TC-8001

## Parsed CVE Data

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
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). This issue is **stream-scoped** to 2.2.x.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. This maps to the **Cargo** ecosystem. The lock file to inspect is `Cargo.lock`, and the check command is `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`.

## Notes

- The current Affects Versions field shows "RHTPA 2.0.0", which does not correspond to any configured version stream (2.1.x or 2.2.x). This will need correction in Step 3.
- The vulnerability is a denial of service (DoS) caused by unbounded stream allocation in QUIC transport frame handling.
