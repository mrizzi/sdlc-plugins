# Step 1 -- Data Extraction: TC-8003

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`), summary text |
| Affected component | `pscomponent:org/rhtpa-server` | Labels (matches component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | `[rhtpa-2.2]` | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | (none found) | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links -- GitHub Advisory |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links -- CVE Record |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | (none) | Issue comment history |
| Issue status | New | Jira `status` field |
| Assignee | Unassigned | Jira `assignee` field |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`.

1. Parsed suffix: `[rhtpa-2.2]` maps to stream **2.2.x**
2. Matched to Version Streams table: stream 2.2.x corresponds to Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.4.z` at local path `/home/dev/repos/rhtpa-release.0.4.z`
3. Issue stream scope: **2.2.x** (scoped to single stream)

Steps 2-7 will be scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, which is a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md:

- **Ecosystem**: Cargo
- **Repository**: backend
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Upstream branch**: `release/0.4.z`

This is a source dependency ecosystem (Cargo), which means remediation would require two tasks: an upstream backport task (source repo fix) and a downstream propagation subtask (Konflux release repo update).

## Vulnerability Summary

quinn-proto versions before 0.11.14 allow a remote attacker to cause a denial of service (DoS) by sending a QUIC transport frame that creates an excessive number of streams. The server panics when the allocation exceeds internal limits. The fix is available in quinn-proto version 0.11.14.

## Additional References

- https://rustsec.org/advisories/RUSTSEC-2026-0042.html
