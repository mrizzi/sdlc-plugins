# Step 1 -- Data Extraction

## Parsed CVE Data for TC-8004

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | _(no stream suffix -- unscoped)_ |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions before 0.4.8 (< 0.4.8) |
| Fixed version | 0.4.8 |
| Upstream fix PR | hyperium/h2#812 |
| Advisory URL | GHSA-2026-kv8p-r3n7 (GitHub Advisory) |
| CVE record URL | CVE-2026-33501 (CVE Record) |
| CVSS | 7.5 (High) |
| Due date | 2026-08-01 |
| Assignee | Unassigned |
| Status | New |

## Stream Scope Resolution

The issue summary ("CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames") contains **no stream suffix** in brackets. Therefore this issue is **unscoped** -- it covers all configured version streams (2.1.x and 2.2.x). Steps 3 and 4 will apply across all streams.

## Ecosystem Detection

The vulnerable library is **h2**, a Rust crate (Cargo ecosystem). The component label `pscomponent:org/rhtpa-server` confirms this is a source dependency in the rhtpa-backend repository. The ecosystem is **Cargo**, which means:

- Lock file: `Cargo.lock`
- Remediation pattern: two tasks (upstream backport + downstream propagation)
