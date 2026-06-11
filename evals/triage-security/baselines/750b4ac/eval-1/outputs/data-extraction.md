# Step 1 -- Data Extraction

## Issue: TC-8001

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (i.e., < 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`. Mapping to configured Version Streams:

- `[rhtpa-2.2]` --> stream **2.2.x**
- Matched to: Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.4.z` (local path: `/home/dev/repos/rhtpa-release.0.4.z`)

**Issue stream scope: 2.2.x only**

Steps 2-7 will be scoped to the 2.2.x stream. Versions from other streams (e.g., 2.1.x) are outside this issue's scope.

## Ecosystem Detection

- **Library**: quinn-proto (Rust crate)
- **Ecosystem**: Cargo
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- **Upstream branch**: `release/0.4.z`
- **Source repository**: backend (rhtpa-backend)

Since this is a **source dependency** (Cargo ecosystem), remediation will require two tasks: an upstream backport task and a downstream propagation subtask.

## Additional References

- RustSec advisory: https://rustsec.org/advisories/RUSTSEC-2026-0042.html
- Vulnerability description: quinn-proto does not properly validate the number of streams requested in a STREAMS frame, allowing a remote attacker to cause a denial of service (panic) by sending a QUIC transport frame that creates an excessive number of stream state objects.
