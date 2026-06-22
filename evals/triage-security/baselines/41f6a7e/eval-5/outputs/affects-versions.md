# Step 3 -- Affects Versions Correction

## Current Affects Versions (PSIRT-assigned)

- **RHTPA 2.0.0**

## Version Impact Evidence (2.2.x stream, scoped by issue suffix [rhtpa-2.2])

| Version | Affected? |
|---------|-----------|
| 2.2.0 | YES |
| 2.2.1 | YES |
| 2.2.2 | YES (retag of 2.2.1) |
| 2.2.3 | NO (ships fixed 3.0.7-28.el9_4) |
| 2.2.4 | NO (ships fixed 3.0.7-28.el9_4) |

## Analysis

The PSIRT-assigned Affects Version "RHTPA 2.0.0" is **incorrect**. There is no 2.0.x stream in the configured Version Streams, and the issue is scoped to the 2.2.x stream. Lock file analysis confirms that versions 2.2.0, 2.2.1, and 2.2.2 ship vulnerable openssl-libs (before 3.0.7-28.el9_4), while versions 2.2.3 and 2.2.4 ship the fixed version.

## Proposed Correction

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

Rationale: Based on rpms.lock.yaml analysis at pinned commits from the supportability matrix. Scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`. Only versions that ship openssl-libs before 3.0.7-28.el9_4 are included.

## Jira Mutation (would execute after engineer confirmation)

```
jira.edit_issue("TC-8005", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-id>"},
    {"id": "<RHTPA-2.2.1-jira-id>"},
    {"id": "<RHTPA-2.2.2-jira-id>"}
  ]
})
```

Note: Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1). The IDs shown above are placeholders.

## Comment (would be posted to TC-8005)

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

Versions 2.2.3+ ship openssl-libs 3.0.7-28.el9_4 (the fixed version) and are not affected.
```
