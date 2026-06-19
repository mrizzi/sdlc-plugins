# Step 1 -- Data Extraction: TC-8004

## Parsed CVE Data

| Field | Value |
|-------|-------|
| **Issue Key** | TC-8004 |
| **CVE ID** | CVE-2026-33501 |
| **Summary** | CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames |
| **Issue Type** | Vulnerability |
| **Status** | New |
| **Affected Component** | `pscomponent:org/rhtpa-server` |
| **Vulnerable Library** | h2 (Rust crate) |
| **Affected Version Range** | versions before 0.4.8 (< 0.4.8) |
| **Fixed Version** | 0.4.8 |
| **CVSS** | 7.5 (High) |
| **Affects Versions (Jira)** | RHTPA 2.1.0, RHTPA 2.2.0 |
| **Due Date** | 2026-08-01 |
| **Assignee** | Unassigned |

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7) |
| CVE Record | [CVE-2026-33501](https://www.cve.org/CVERecord?id=CVE-2026-33501) |
| Upstream Fix PR | [hyperium/h2#812](https://github.com/hyperium/h2/pull/812) |

## Additional References

- https://rustsec.org/advisories/RUSTSEC-2026-0055.html

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" contains **no stream suffix** in brackets. Therefore this issue is **unscoped** -- it covers all configured version streams.

All streams must be analyzed:
- **2.1.x** (Konflux release repo: rhtpa-release.0.3.z)
- **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)

## Ecosystem Detection

- **Library**: h2 (Rust crate)
- **Ecosystem**: Cargo
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Upstream branches**:
  - 2.1.x stream: `release/0.3.z`
  - 2.2.x stream: `release/0.4.z`

Since h2 is a Cargo (source dependency) ecosystem, remediation requires **two tasks** per affected stream: an upstream backport task (source repo fix) and a downstream propagation subtask (Konflux release repo update).

## Existing Comments

No comments on the issue.
