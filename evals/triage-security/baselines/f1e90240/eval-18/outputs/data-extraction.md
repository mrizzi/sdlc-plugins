# Step 1 -- Data Extraction for TC-8001

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels (`CVE-2026-31812`) and summary text |
| Affected component | pscomponent:org/rhtpa-server | Label matching `pscomponent:` pattern |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Status | In Progress | Issue status |
| Assignee | engineer-a@example.com | Issue assignee |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server, ai-cve-triaged | Issue labels |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table row: `2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Scope: **single-stream** -- Steps 3-8 are scoped to stream 2.2.x only

## Ecosystem Detection

- Vulnerable library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- Upstream branch: `release/0.4.z`

## Existing Comments (from prior triage run)

1. **Description digest comment**: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2`
   - Posted by: sdlc-workflow/triage-security
   - Created: 2026-07-01T10:00:00Z

2. **Post-triage summary comment**: Documents version impact (RHTPA 2.2.0 and 2.2.1 affected, 2.2.2+ not affected), actions taken (Affects Versions corrected, label added, remediation tasks TC-8100 and TC-8101 created, transitioned to In Progress)
   - Posted by: sdlc-workflow/triage-security
   - Created: 2026-07-01T10:01:00Z

## Existing Issue Links (from prior triage run)

| Link Type | Linked Issue | Summary | Status |
|-----------|-------------|---------|--------|
| Depend | TC-8100 | Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2] | In Progress |
| Depend | TC-8101 | Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2] | Open |

TC-8101 is blocked by TC-8100 (upstream backport must merge first).

## Version Impact Table (from security-matrix-mock.md)

Using the mock lock file data for quinn-proto versions:

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | Outside issue scope |
| 2.1.1 | 2.1.x | 0.11.9 | YES | Outside issue scope |
| 2.2.0 | 2.2.x | 0.11.9 | YES | In scope |
| 2.2.1 | 2.2.x | 0.11.12 | YES | In scope |
| 2.2.2 | 2.2.x | -- | YES | Retag of 2.2.1 (same as v0.4.8 = 0.11.12) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | Fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | Fixed version |

Fix threshold: quinn-proto >= 0.11.14 (not affected). Versions shipping < 0.11.14 are affected.
