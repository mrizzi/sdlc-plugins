# Step 1 — Data Extraction: TC-8030

## Extracted Fields

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-48901 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (pscomponent: pattern) |
| Product version (PSIRT-claimed) | [rhtpa-2.2] | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | h2 | Description text |
| Affected version range | "versions prior to the fix" (imprecise) | Description text |
| Fixed version | "see advisory" (imprecise) | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-r7f2-kk9p | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-48901 | Remote links |
| Due date | 2026-08-01 | Jira `duedate` field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Local path: /home/dev/repos/rhtpa-release.0.4.z
- Issue stream scope: **scoped to 2.2.x only**

## Ecosystem Detection

- Vulnerable library: **h2** (Rust crate on crates.io)
- Detected ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`

## Data Quality Flags

- **Affected version range is imprecise**: Jira description says "versions prior to the fix" with no precise version threshold. External CVE data enrichment (Step 1.5) is required to establish a machine-readable fix threshold.
- **Fixed version is imprecise**: Jira description says "see advisory" without specifying the exact fixed version. External CVE data enrichment (Step 1.5) is required.

## Deployment Context

- Affected repository: rhtpa-backend
- Deployment context: **upstream** (from Source Repositories table)
