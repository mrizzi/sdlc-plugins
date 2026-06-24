# Step 3 -- Affects Versions Correction

## Current State

- PSIRT-assigned Affects Versions: `RHTPA 2.0.0`
- Issue stream scope: **2.2.x** (from suffix `[rhtpa-2.2]`)

## Version Impact (scoped to 2.2.x stream)

| Version | Affected? |
|---------|-----------|
| RHTPA 2.2.0 | YES |
| RHTPA 2.2.1 | YES |
| RHTPA 2.2.2 | YES (retag of 2.2.1) |
| RHTPA 2.2.3 | NO |
| RHTPA 2.2.4 | NO |

## Correction

The PSIRT-assigned version `RHTPA 2.0.0` is incorrect -- there is no 2.0.x stream in the configured Version Streams, and lock file analysis shows that the affected versions in the 2.2.x stream are 2.2.0, 2.2.1, and 2.2.2.

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

Rationale: Based on rpms.lock.yaml analysis at pinned commits from the 2.2.x supportability matrix:
- RHTPA 2.2.0 (v0.4.5): openssl-libs 3.0.7-25.el9_3 -- vulnerable (below 3.0.7-28.el9_4)
- RHTPA 2.2.1 (v0.4.8): openssl-libs 3.0.7-27.el9_4 -- vulnerable (below 3.0.7-28.el9_4)
- RHTPA 2.2.2 (v0.4.9): retag of v0.4.8 -- same as 2.2.1, vulnerable
- RHTPA 2.2.3 (v0.4.11): openssl-libs 3.0.7-28.el9_4 -- NOT vulnerable (at fix threshold)
- RHTPA 2.2.4 (v0.4.12): openssl-libs 3.0.7-28.el9_4 -- NOT vulnerable (at fix threshold)

Scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`.

## Jira Mutation (would execute after engineer confirmation)

```
jira.edit_issue("TC-8005", fields={
  "versions": [
    {"id": "<jira-id-for-RHTPA-2.2.0>"},
    {"id": "<jira-id-for-RHTPA-2.2.1>"},
    {"id": "<jira-id-for-RHTPA-2.2.2>"}
  ]
})
```

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields`.

## Comment (would post after engineer confirmation)

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
```
