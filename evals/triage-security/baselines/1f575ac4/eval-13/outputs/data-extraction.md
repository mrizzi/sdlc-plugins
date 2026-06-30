# Step 1 -- Data Extraction for TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] (stream suffix) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | (no comments) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x. Steps 3-7 apply only to versions within the 2.2.x stream.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, which is a Rust crate. Based on the Ecosystem Mappings tables in security-matrix.md, the ecosystem is **Cargo**. The lock file is `Cargo.lock` and the check command is `git show <tag>:Cargo.lock`.

## PSIRT Affects Versions Issue

The PSIRT-assigned Affects Version is **RHTPA 2.0.0**, but there is no 2.0.x stream configured in the Version Streams table. The configured streams are 2.1.x and 2.2.x. This is an incorrect Affects Version that will need correction in Step 3.

## Additional References

- RustSec: https://rustsec.org/advisories/RUSTSEC-2026-0042.html
- GitHub Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq
