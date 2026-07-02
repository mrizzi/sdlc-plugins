# Step 3 -- Affects Versions Correction

## Current vs Proposed Affects Versions

**PROPOSAL: Correct the Affects Versions on TC-8001.**

The issue is scoped to the **2.2.x** stream (from the `[rhtpa-2.2]` summary
suffix). Only versions belonging to the 2.2.x stream are included in the
correction. The 2.1.x versions (2.1.0, 2.1.1) are also affected but belong
to a companion issue's scope (see Step 4 cross-stream coordination).

### Correction Details

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

**Rationale**: The PSIRT-assigned Affects Version "RHTPA 2.0.0" is incorrect.
There is no RHTPA 2.0.0 in the supportability matrix -- this version does not
exist in any configured version stream. Based on lock file analysis at pinned
commits from security-matrix.md:

| Version | Backend Tag | quinn-proto | Affected? | In Scope (2.2.x)? |
|---------|-------------|-------------|-----------|---------------------|
| 2.2.0 | `v0.4.5` | 0.11.9 | YES | YES |
| 2.2.1 | `v0.4.8` | 0.11.12 | YES | YES |
| 2.2.2 | `v0.4.9` | (retag of v0.4.8) | YES | YES |
| 2.2.3 | `v0.4.11` | 0.11.14 | NO | -- |
| 2.2.4 | `v0.4.12` | 0.11.14 | NO | -- |

Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and
are excluded from Affects Versions.

### Proposed Jira Mutation

After engineer confirmation, the following update would be executed:

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<jira-id-for-RHTPA-2.2.0>"},
    {"id": "<jira-id-for-RHTPA-2.2.1>"},
    {"id": "<jira-id-for-RHTPA-2.2.2>"}
  ]
})
```

Note: Jira version IDs would be discovered dynamically via
`getJiraIssueTypeMetaWithFields` (Step 3.1). The IDs shown as placeholders
above would be replaced with actual values from the Jira version registry.

### Proposed Comment

A comment would be posted to TC-8001 documenting the correction:

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

RHTPA 2.0.0 does not exist in the supportability matrix. Versions 2.2.0,
2.2.1, and 2.2.2 ship quinn-proto < 0.11.14 and are vulnerable. Versions
2.2.3+ ship the fixed version (0.11.14).
```
