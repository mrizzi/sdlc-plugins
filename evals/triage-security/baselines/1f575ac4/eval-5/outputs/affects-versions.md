# Step 3 -- Affects Versions Correction

## Current vs Proposed Affects Versions

**Issue**: TC-8005 (scoped to stream 2.2.x)

| | Affects Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.0.0 |
| **Proposed (lock file evidence)** | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

The PSIRT-assigned Affects Version `RHTPA 2.0.0` is incorrect -- there is no 2.0.x stream configured in the Version Streams table. The version impact analysis from Step 2 shows that within the 2.2.x stream:

- **RHTPA 2.2.0** -- ships openssl-libs 3.0.7-25.el9_3 (vulnerable, below fix threshold 3.0.7-28.el9_4)
- **RHTPA 2.2.1** -- ships openssl-libs 3.0.7-27.el9_4 (vulnerable, below fix threshold 3.0.7-28.el9_4)
- **RHTPA 2.2.2** -- retag of 2.2.1, ships openssl-libs 3.0.7-27.el9_4 (vulnerable)
- **RHTPA 2.2.3** -- ships openssl-libs 3.0.7-28.el9_4 (not affected, ships fixed version)
- **RHTPA 2.2.4** -- ships openssl-libs 3.0.7-28.el9_4 (not affected, ships fixed version)

The correction is scoped to the 2.2.x stream per the issue suffix `[rhtpa-2.2]`. Only versions 2.2.0, 2.2.1, and 2.2.2 are affected within this stream.

## Proposed Jira Mutation

```
jira.edit_issue("TC-8005", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-id>"},
    {"id": "<RHTPA-2.2.1-jira-id>"},
    {"id": "<RHTPA-2.2.2-jira-id>"}
  ]
})
```

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (not hardcoded).

## Proposed Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

Versions 2.2.3 and 2.2.4 ship the patched openssl-libs 3.0.7-28.el9_4 and are not affected.
```
