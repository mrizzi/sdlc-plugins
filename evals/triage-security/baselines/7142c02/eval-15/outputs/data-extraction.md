# Step 1 -- Data Extraction: TC-8001

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Stream scope | 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |
| Reporter | psirt-analyst (account ID: 557058:psirt-analyst-mock-id) |
| Ecosystem | Cargo (Rust crate) |

## Stream Scope Resolution

The issue summary contains `[rhtpa-2.2]`, which maps to the **2.2.x** version stream
(Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x. Steps 3-7 apply only to this stream,
though cross-stream impact on 2.1.x will be reported in Step 7 Case B.

## Vulnerability Description

quinn-proto crate before version 0.11.14 allows a remote attacker to cause a panic
by sending a QUIC transport frame that creates an excessive number of streams. This
is classified as a denial of service (DoS) vulnerability. The vulnerability exists
because quinn-proto does not properly validate the number of streams requested in a
STREAMS frame, leading to unbounded allocation and eventual panic.
