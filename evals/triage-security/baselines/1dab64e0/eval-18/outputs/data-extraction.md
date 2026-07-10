# Step 1 -- Data Extraction for TC-8001

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Assignee | engineer-a@example.com |
| Status | In Progress |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server, ai-cve-triaged |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams row: 2.2.x -> rhtpa-release.0.4.z)
- Issue stream scope: **2.2.x only**

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`

## Existing Comments on Issue

1. **Description digest comment**: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2` -- posted by sdlc-workflow/triage-security on 2026-07-01T10:00:00Z
2. **Post-triage summary comment**: Documents version impact (RHTPA 2.2.0 and 2.2.1 affected, 2.2.2+ not affected), Affects Versions correction, ai-cve-triaged label addition, remediation tasks TC-8100 and TC-8101, and transition to In Progress -- posted by sdlc-workflow/triage-security on 2026-07-01T10:01:00Z

## Existing Issue Links

- **Depend**: TC-8100 (upstream backport task -- In Progress)
- **Depend**: TC-8101 (downstream propagation task -- Open, blocks TC-8100)

## Remote Links

- GitHub Advisory: GHSA-2026-qp73-x4mq
- CVE Record: CVE-2026-31812
- Upstream fix PR: quinn-rs/quinn#2048

## Version Impact (from security-matrix mock data, stream 2.2.x only)

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | v0.4.9 | (retag of v0.4.8) | YES | same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |
