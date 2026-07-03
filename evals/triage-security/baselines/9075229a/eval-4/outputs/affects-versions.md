# Affects Versions Correction — TC-8004

## Current vs Proposed

The issue is **unscoped** (no stream suffix), so the Affects Versions correction includes all affected versions across all streams.

```
Current (PSIRT-assigned): [RHTPA 2.1.0, RHTPA 2.2.0]
Proposed (lock file evidence): [RHTPA 2.1.0, RHTPA 2.1.1]
```

## Changes

| Action | Version | Reason |
|--------|---------|--------|
| Keep | RHTPA 2.1.0 | Affected — ships h2 0.4.5 (< 0.4.8) |
| Add | RHTPA 2.1.1 | Affected — ships h2 0.4.5 (< 0.4.8); missing from PSIRT assignment |
| Remove | RHTPA 2.2.0 | NOT affected — ships h2 0.4.8 (= fix version); incorrectly included by PSIRT |

## Rationale

PSIRT assigned Affects Versions based on scan time, not actual dependency analysis. Lock file inspection at pinned source commits from the supportability matrix shows:

- **RHTPA 2.1.0** (tag `v0.3.8`): h2 0.4.5 -- AFFECTED (below fix threshold 0.4.8)
- **RHTPA 2.1.1** (tag `v0.3.12`): h2 0.4.5 -- AFFECTED (below fix threshold 0.4.8)
- **RHTPA 2.2.0** (tag `v0.4.5`): h2 0.4.8 -- NOT AFFECTED (ships the fix version)

PSIRT omitted RHTPA 2.1.1 (affected) and incorrectly included RHTPA 2.2.0 (not affected).

## Jira Mutation (requires engineer confirmation)

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"id": "<RHTPA-2.1.0-jira-id>"},
    {"id": "<RHTPA-2.1.1-jira-id>"}
  ]
})
```

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1). No hardcoded IDs.

## Comment (to be posted after correction)

```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
Based on lock file analysis at pinned commits from security-matrix.md.

- Removed RHTPA 2.2.0: ships h2 0.4.8 (fix version) — not affected.
- Added RHTPA 2.1.1: ships h2 0.4.5 (< 0.4.8) — affected.

Issue is unscoped (no stream suffix) — correction spans all streams.
```
