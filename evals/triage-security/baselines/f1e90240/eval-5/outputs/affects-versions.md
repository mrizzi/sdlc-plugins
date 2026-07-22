# Step 3 -- Affects Versions Correction: TC-8005

## Current vs Proposed

| | Affects Versions |
|---|---|
| Current (PSIRT-assigned) | RHTPA 2.0.0 |
| Proposed (lock file evidence) | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

The PSIRT-assigned Affects Version `RHTPA 2.0.0` is incorrect -- version 2.0.0
does not appear in the supportability matrix for any configured stream. The
issue is scoped to the 2.2.x stream (per summary suffix `[rhtpa-2.2]`), so
only versions within the 2.2.x stream are included in the correction.

Lock file analysis at pinned commits from security-matrix.md shows:

- **RHTPA 2.2.0** (tag v0.4.5): openssl-libs 3.0.7-25.el9_3 -- AFFECTED (before 3.0.7-28.el9_4)
- **RHTPA 2.2.1** (tag v0.4.8): openssl-libs 3.0.7-27.el9_4 -- AFFECTED (before 3.0.7-28.el9_4)
- **RHTPA 2.2.2** (tag v0.4.9): retag of 2.2.1 -- AFFECTED (same as 2.2.1)
- **RHTPA 2.2.3** (tag v0.4.11): openssl-libs 3.0.7-28.el9_4 -- NOT AFFECTED (equals fixed version)
- **RHTPA 2.2.4** (tag v0.4.12): openssl-libs 3.0.7-28.el9_4 -- NOT AFFECTED (equals fixed version)

Versions 2.1.0 and 2.1.1 are also affected but belong to the 2.1.x stream,
which is outside this issue's scope. Cross-stream impact is reported via
Case B (Step 8).

## Proposed Jira Update

```
jira.edit_issue("TC-8005", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-id>"},
    {"id": "<RHTPA-2.2.1-jira-id>"},
    {"id": "<RHTPA-2.2.2-jira-id>"}
  ]
})
```

Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields`.

## Proposed Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] --> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
RHTPA 2.0.0 does not exist in any configured version stream.
```
