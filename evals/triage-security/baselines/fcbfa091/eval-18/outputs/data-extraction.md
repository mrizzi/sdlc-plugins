# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Assignee | engineer-a@example.com |
| Issue status | In Progress |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server, ai-cve-triaged |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams row: 2.2.x at `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Scope: **single stream** -- only the 2.2.x stream is in scope for this issue

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`

## Existing Comments Detected

1. **Description digest comment** -- `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2` (posted 2026-07-01T10:00:00Z by sdlc-workflow/triage-security)
2. **Post-triage summary comment** -- Documents version impact, Affects Versions correction, and remediation tasks TC-8100/TC-8101 (posted 2026-07-01T10:01:00Z by sdlc-workflow/triage-security)

## Existing Issue Links Detected

- **Depend**: TC-8100 -- "Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2]" (In Progress, labels: ai-generated-jira, Security, CVE-2026-31812)
- **Depend**: TC-8101 -- "Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2]" (Open, labels: ai-generated-jira, Security, CVE-2026-31812, blocks TC-8100)

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: upstream (default -- no Deployment Context column in Source Repositories table)
