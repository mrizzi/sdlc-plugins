# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| Upstream fix PR | quinn-rs/quinn#2048 |
| Advisory URL | GHSA-2026-qp73-x4mq |
| CVE record URL | CVE-2026-31812 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x stream** (rhtpa-release.0.4.z). This issue is scoped to the 2.2.x stream for Affects Versions correction (Step 3) and remediation task creation (Step 7).

However, per Important Rule 4, **all versions across all streams** (2.1.x and 2.2.x) must be checked for version impact analysis in Step 2.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The ecosystem is **Cargo**, confirmed by the Ecosystem Mappings tables in both streams which list Cargo with `Cargo.lock` as the lock file. This means:

- Lock file: `Cargo.lock`
- Check command: `git show tag:Cargo.lock`
- Remediation pattern: **Two tasks** (upstream backport + downstream propagation subtask with Blocks dependency)
