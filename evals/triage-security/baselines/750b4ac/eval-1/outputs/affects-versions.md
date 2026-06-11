# Step 3 -- Affects Versions Correction

## Current vs Proposed Affects Versions

The PSIRT-assigned Affects Versions on TC-8001 is incorrect. The issue carries "RHTPA 2.0.0" but there is no 2.0.x version stream -- the issue is scoped to stream 2.2.x per the summary suffix `[rhtpa-2.2]`.

### Diff

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

### Rationale

Based on lock file analysis at pinned commits from security-matrix.md, scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`:

| Version | quinn-proto | Affected? | Include in Affects Versions? |
|---------|-------------|-----------|------------------------------|
| RHTPA 2.2.0 | 0.11.9 | YES | YES |
| RHTPA 2.2.1 | 0.11.12 | YES | YES |
| RHTPA 2.2.2 | -- (retag of 2.2.1) | YES | YES |
| RHTPA 2.2.3 | 0.11.14 | NO | NO -- ships fixed version |
| RHTPA 2.2.4 | 0.11.14 | NO | NO -- ships fixed version |

### Why "RHTPA 2.0.0" is Wrong

- There is no `2.0.x` version stream in the Security Configuration
- The issue summary suffix `[rhtpa-2.2]` indicates PSIRT intended this for the 2.2.x stream
- PSIRT likely assigned "RHTPA 2.0.0" based on scan-time metadata rather than actual dependency analysis
- "RHTPA 2.0.0" must be removed and replaced with the actually affected 2.2.x versions

### Versions Excluded

- **RHTPA 2.1.0, RHTPA 2.1.1** -- These are affected (quinn-proto 0.11.9) but belong to the 2.1.x stream. This issue is scoped to 2.2.x only; the 2.1.x stream would be tracked by a separate companion Vulnerability issue.
- **RHTPA 2.2.3, RHTPA 2.2.4** -- Not affected; these versions ship quinn-proto 0.11.14 (the fixed version).

### Proposed Jira Mutation (requires engineer confirmation)

```
PROPOSAL: jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-id>"},
    {"id": "<RHTPA-2.2.1-jira-id>"},
    {"id": "<RHTPA-2.2.2-jira-id>"}
  ]
})
```

Note: Jira version IDs (shown as placeholders above) would be discovered dynamically at runtime via `getJiraIssueTypeMetaWithFields` for the Vulnerability issue type. The version names (RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2) are matched against the `allowedValues` returned by the API to resolve their IDs.

### Proposed Comment

```
PROPOSAL: jira.add_comment("TC-8001",
  "Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
  Based on lock file analysis at pinned commits from security-matrix.md.
  Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].")
```
