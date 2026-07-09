# Step 1 -- Data Extraction: TC-8001

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
| Upstream fix PR | quinn-rs/quinn#2048 (https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | GHSA-2026-qp73-x4mq (https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Assignee | engineer-a@example.com |
| Status | In Progress |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server, ai-cve-triaged |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry: rhtpa-release.0.4.z)
- Issue is **stream-scoped** to the 2.2.x stream only.

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`

## Deployment Context

- Source repository: rhtpa-backend
- Deployment context: upstream (default -- no Deployment Context column in Source Repositories)

## Existing Issue Links

| Link Type | Issue | Summary | Status |
|-----------|-------|---------|--------|
| Depend | TC-8100 | Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2] | In Progress |
| Depend | TC-8101 | Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2] | Open |

## Existing Remote Links

| Title | URL |
|-------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |

## Existing Comments

1. Description digest comment: `sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2` (posted 2026-07-01T10:00:00Z)
2. Post-triage summary comment documenting version impact, Affects Versions correction, remediation tasks TC-8100 and TC-8101, and transition to In Progress (posted 2026-07-01T10:01:00Z)

## Version Impact (from security-matrix mock data)

The scoped stream is 2.2.x (rhtpa-release.0.4.z). quinn-proto versions by tag:

| Version | Build Tag | quinn-proto version | Affected? |
|---------|-----------|---------------------|-----------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES (< 0.11.14) |
| 2.2.1 | v0.4.8 | 0.11.12 | YES (< 0.11.14) |
| 2.2.2 | v0.4.9 | (retag of v0.4.8) = 0.11.12 | YES (< 0.11.14) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO (= 0.11.14, fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO (= 0.11.14, fixed) |

Conclusion: RHTPA 2.2.0, 2.2.1, and 2.2.2 are affected. RHTPA 2.2.3 and 2.2.4 are not affected (they ship the fixed version 0.11.14).

Note: The current Affects Versions on the issue (RHTPA 2.2.0, RHTPA 2.2.1) were already corrected during the prior triage run. RHTPA 2.2.2 is also technically affected (retag of 2.2.1) but may have been intentionally excluded if it was already superseded.
