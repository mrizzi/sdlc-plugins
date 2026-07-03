# Version Impact Analysis — CVE-2026-55123

## Version Impact Table

Version Impact for CVE-2026-55123 (tokio < 1.42.0, fixed in 1.42.0):

| Version     | Stream    | tokio version | Affected? | Notes |
|-------------|-----------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0        | YES       |       |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0        | YES       |       |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1        | YES       |       |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1        | YES       |       |

All versions across both streams ship tokio below the fix threshold of 1.42.0.

## Cross-Stream Impact

The issue is scoped to stream **rhtpa-2.2** (per the `[rhtpa-2.2]` suffix), but the version impact analysis reveals that stream **rhtpa-2.1** is also affected:

- **rhtpa-2.1**: tokio 1.40.0 (affected -- below fix threshold 1.42.0)
- **rhtpa-2.2**: tokio 1.41.1 (affected -- below fix threshold 1.42.0)

### Stream-Scoped Affects Versions (for this issue)

Since TC-8020 is scoped to stream rhtpa-2.2, only the 2.2.x versions apply to this issue:

| Version     | Affected? |
|-------------|-----------|
| RHTPA 2.2.0 | YES       |
| RHTPA 2.2.1 | YES       |

The 2.1.x versions (RHTPA 2.1.0, RHTPA 2.1.1) are out of scope for this issue and belong to a sibling CVE Jira for the rhtpa-2.1 stream.

## Sibling CVE Jira Search (Step 4)

JQL: `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020`

**Result**: No sibling Vulnerability issues found for CVE-2026-55123 in stream rhtpa-2.1. No CVE Jira exists for the rhtpa-2.1 stream.

## Ecosystem Details

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | Cargo.lock | `git show <tag>:Cargo.lock` | release/0.3.z (2.1.x), release/0.4.z (2.2.x) |

## Source Pinning

- **backend**: `artifacts.lock.yaml` (download URL contains tag)
