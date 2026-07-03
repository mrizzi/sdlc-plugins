# Step 1 -- Data Extraction

## Extracted CVE Data for TC-8030

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-48901 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | "versions prior to the fix" (imprecise -- no exact threshold in Jira description) |
| Fixed version | "see advisory" (imprecise -- no exact threshold in Jira description) |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 |
| Due date | 2026-08-01 |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Matched Version Stream: 2.2.x (Konflux release repo: git.example.com/rhtpa/rhtpa-release.0.4.z)
- Issue stream scope: **2.2.x only**

## Ecosystem Detection

- Library: h2 (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z` (for 2.2.x stream)

## Deployment Context Lookup

- Affected repository: rhtpa-backend
- Source Repositories table match: rhtpa-backend (URL: https://github.com/rhtpa/rhtpa-backend)
- Deployment Context column: **absent** (backward compatibility -- default to `upstream`, coordination guidance omitted)

## Data Quality Notes

The Jira description provides **imprecise** version information:
- Affected versions: "versions prior to the fix" -- no exact version threshold
- Fixed version: "see advisory" -- no specific version number

External CVE data enrichment (Step 1.5) is required to establish the precise fix threshold for version impact analysis.
