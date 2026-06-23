# Step 1 -- Data Extraction for TC-8006

## Extracted Fields

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Affects Versions (Jira field) | RHTPA 2.1.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| Upstream fix PR | (none found in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | (none) |
| CVSS | 7.5 (High) |
| Status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.1]`. This maps to the **2.1.x** version stream in the Security Configuration Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |

**Issue stream scope**: 2.1.x (scoped issue -- Steps 3-4 apply only to this stream's versions).

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. From the 2.1.x stream's security-matrix.md Ecosystem Mappings table:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | Cargo.lock | `git show <tag>:Cargo.lock` | release/0.3.z |

**Ecosystem**: Cargo (source dependency -- remediation requires two tasks: upstream backport + downstream propagation).

## Existing Issue Links

The following links already exist on TC-8006:

- **Related** (outward): TC-8001 -- CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] (Link ID: 1990401)

## Version Impact Table (Stream 2.1.x -- issue scope)

Based on the mock lock file data from the security matrix:

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | v0.3.8 -- vulnerable (< 0.11.14) |
| 2.1.1 | 0.11.9 | YES | v0.3.12 -- vulnerable (< 0.11.14) |

Both versions in the 2.1.x stream ship quinn-proto 0.11.9, which is below the fixed version 0.11.14. All versions in the issue's stream scope are affected.

## Cross-Stream Impact (informational, outside issue scope)

For completeness, the 2.2.x stream impact (tracked by sibling TC-8001):

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | v0.4.5 -- vulnerable |
| 2.2.1 | 0.11.12 | YES | v0.4.8 -- vulnerable |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 0.11.14 | NO | v0.4.11 -- fixed |
| 2.2.4 | 0.11.14 | NO | v0.4.12 -- fixed |

The 2.2.x stream is tracked by sibling TC-8001 and is outside the scope of TC-8006.

## Upstream Fix Status (Stream 2.1.x)

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | (would need git show to determine) | TBD |

Note: In a live triage, `git show release/0.3.z:Cargo.lock` would be run against the backend source repo to check whether the upstream branch already carries the fix.
