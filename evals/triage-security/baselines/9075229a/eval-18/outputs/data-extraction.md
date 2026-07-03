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
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| CVSS | 7.5 (High) |
| Existing comments | 2 comments (description digest + post-triage summary) |

## Stream Scope Resolution

Summary suffix `[rhtpa-2.2]` maps to configured Version Stream **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x only. Steps 3-4 will apply only to this stream.

## Ecosystem Detection

Vulnerable library `quinn-proto` is a Rust crate. Ecosystem: **Cargo**.

The 2.2.x stream's `security-matrix.md` Ecosystem Mappings table confirms Cargo is a supported ecosystem with:
- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`

## Deployment Context

The Source Repositories table in the mock CLAUDE.md does not include a Deployment Context column. Per the skill's backward-compatibility rule, all repositories default to `upstream`.

## Existing Issue Links

| Link Type | Issue | Summary | Status |
|-----------|-------|---------|--------|
| Depend | TC-8100 | Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2] | In Progress |
| Depend | TC-8101 | Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2] | Open |

## Existing Labels

- CVE-2026-31812
- pscomponent:org/rhtpa-server
- ai-cve-triaged

## Existing Comments

1. Description digest comment: `sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2` (posted 2026-07-01T10:00:00Z)
2. Post-triage summary comment documenting version impact, actions taken, and remediation tasks (posted 2026-07-01T10:01:00Z)
