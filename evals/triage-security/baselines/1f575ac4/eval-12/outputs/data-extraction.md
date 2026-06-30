# Step 1 -- Data Extraction: TC-8030

## Parsed Fields

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions prior to the fix (imprecise -- no exact threshold in Jira description) |
| Fixed version | see advisory (imprecise -- no exact version in Jira description) |
| CVSS | 7.5 (High) |
| Due date | 2026-08-01 |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Scope: analysis is scoped to the 2.2.x stream; other streams checked for cross-stream impact

## Ecosystem Detection

- Library: h2 (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`
- Upstream branch: `release/0.4.z`

## Data Quality Note

The Jira description provides only imprecise version information:
- Affected range: "versions prior to the fix" -- no numeric threshold
- Fixed version: "see advisory" -- no specific version number

External CVE data enrichment (Step 1.5) is required to obtain a precise fix threshold for version impact analysis.
