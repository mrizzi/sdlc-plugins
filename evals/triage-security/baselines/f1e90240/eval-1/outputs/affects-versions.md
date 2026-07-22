# Step 3 -- Affects Versions Correction

## Current State

- **Current Affects Versions**: RHTPA 2.0.0
- **Issue stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)

## Analysis

The PSIRT-assigned Affects Version `RHTPA 2.0.0` is incorrect. There is no
2.0.x version stream in the configured Version Streams. The issue is scoped
to stream 2.2.x, and the version impact analysis shows the following 2.2.x
versions are affected:

- **RHTPA 2.2.0** -- ships quinn-proto 0.11.9 (vulnerable, < 0.11.14)
- **RHTPA 2.2.1** -- ships quinn-proto 0.11.12 (vulnerable, < 0.11.14)
- **RHTPA 2.2.2** -- retag of 2.2.1, ships quinn-proto 0.11.12 (vulnerable, < 0.11.14)

Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and
are NOT affected.

Versions 2.1.0 and 2.1.1 are also affected but belong to the 2.1.x stream,
which is outside this issue's scope. They are not included in the Affects
Versions correction for this issue.

## Proposed Correction

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

## Jira Mutation (after engineer confirmation)

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<jira-id-for-RHTPA-2.2.0>"},
    {"id": "<jira-id-for-RHTPA-2.2.1>"},
    {"id": "<jira-id-for-RHTPA-2.2.2>"}
  ]
})
```

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields`
for the Vulnerability issue type (type ID 10024) in project TC, filtered by the
Jira version prefix `RHTPA`.

## Comment

```
jira.add_comment("TC-8001",
  "Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
   Based on lock file analysis at pinned commits from security-matrix.md.
   Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
   RHTPA 2.0.0 does not correspond to any configured version stream.")
```
