# Step 1 -- Data Extraction for TC-8021

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches `pscomponent:` pattern from Security Configuration) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comments |
| Upstream Affected Component (customfield_10632) | quinn-proto | Custom field on the issue |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

**Issue stream scope**: 2.2.x (scoped to this single stream for Steps 3-8).

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. From the 2.2.x stream's security-matrix.md Ecosystem Mappings table:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

**Detected ecosystem**: Cargo (source dependency)
**Lock file**: `Cargo.lock`
**Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
**Upstream branch**: `release/0.4.z`

## Deployment Context Lookup

The affected repository (rhtpa-backend) is listed in the Source Repositories table. No Deployment Context column is present in the mock configuration, so the default deployment context of `upstream` applies.

## Version Impact Analysis (Step 2)

Using the mock lock file data from the security matrix, quinn-proto versions at each pinned commit:

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

### Stream 2.2.x (rhtpa-release.0.4.z) -- Issue Scoped Stream

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (ships fixed version) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (ships fixed version) |

### Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD (latest tag) | Fixed? |
|--------|-----------|-----------------|------------------------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (at v0.4.12) | YES |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (at v0.3.12) | NO |

The upstream branch `release/0.4.z` already ships quinn-proto 0.11.14, confirming the fix was incorporated starting from build v0.4.11 (version 2.2.3). The upstream branch `release/0.3.z` still ships 0.11.9 (vulnerable).

## Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, which does not correspond to any configured version stream (no 2.0.x stream exists). This is incorrect.

Based on lock file evidence scoped to the 2.2.x stream:
- **Current**: [RHTPA 2.0.0]
- **Proposed**: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14 (the fixed version). The 2.1.x versions are excluded from this correction because the issue is scoped to the 2.2.x stream; the 2.1.x impact is handled as cross-stream (Case B).
