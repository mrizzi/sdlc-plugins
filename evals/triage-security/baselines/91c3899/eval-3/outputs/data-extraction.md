# Step 1 -- Data Extraction for TC-8003

## Parsed CVE Data

| Field | Value |
|-------|-------|
| **Issue Key** | TC-8003 |
| **CVE ID** | CVE-2026-31812 |
| **Affected Component** | pscomponent:org/rhtpa-server |
| **Product Version (PSIRT-claimed)** | [rhtpa-2.2] |
| **Affects Versions (Jira field)** | RHTPA 2.2.0 |
| **Vulnerable Library** | quinn-proto |
| **Affected Version Range** | versions before 0.11.14 |
| **Fixed Version** | 0.11.14 |
| **CVSS Score** | 7.5 (High) |
| **Advisory URL** | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| **CVE Record URL** | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| **Due Date** | 2026-07-15 |
| **Existing Comments** | None |
| **Status** | New |
| **Assignee** | Unassigned |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration.

- **Summary suffix**: `[rhtpa-2.2]`
- **Mapped stream**: 2.2.x
- **Konflux release repo**: git.example.com/rhtpa/rhtpa-release.0.4.z
- **Local path**: /home/dev/repos/rhtpa-release.0.4.z

The issue is **stream-scoped** to the 2.2.x stream. Steps 3-4 will apply only to versions within this stream.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, which is a Rust crate. Based on the Ecosystem Mappings in the security matrix for the 2.2.x stream:

- **Ecosystem**: Cargo
- **Repository**: backend
- **Lock File**: `Cargo.lock`
- **Check Command**: `git show <tag>:Cargo.lock`
- **Upstream Branch**: `release/0.4.z`

As a source dependency (Cargo), remediation would normally require two tasks: an upstream backport task and a downstream propagation subtask. However, the duplicate check in Step 4 may short-circuit this flow.

## Vulnerability Details

The quinn-proto crate before version 0.11.14 allows a remote attacker to cause a panic by sending a QUIC transport frame that creates an excessive number of streams. This vulnerability is classified as a denial of service (DoS). The vulnerability exists because quinn-proto does not properly validate the number of streams requested in a STREAMS frame.

### References

- GitHub Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq
- RustSec Advisory: https://rustsec.org/advisories/RUSTSEC-2026-0042.html
