# Step 3 -- Affects Versions Correction

## Stream Scope

This issue is scoped to the **2.2.x** stream (from summary suffix `[rhtpa-2.2]`). The Affects Versions correction only includes versions belonging to the 2.2.x stream. The 2.1.x versions (2.1.0, 2.1.1) are also affected but belong to a sibling issue's scope (see Step 4 cross-stream coordination).

## Current vs Proposed

| | Affects Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.0.0 |
| **Proposed (lock file evidence)** | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

The PSIRT-assigned Affects Version **RHTPA 2.0.0** is incorrect:
- There is no 2.0.x version stream configured in the project's Security Configuration.
- RHTPA 2.0.0 does not correspond to any version in the supportability matrix.
- The issue summary suffix `[rhtpa-2.2]` indicates this issue tracks the 2.2.x stream.

Based on lock file analysis at pinned commits from security-matrix.md:
- **RHTPA 2.2.0** (build v0.4.5): ships quinn-proto 0.11.9 -- AFFECTED
- **RHTPA 2.2.1** (build v0.4.8): ships quinn-proto 0.11.12 -- AFFECTED
- **RHTPA 2.2.2** (build v0.4.9): retag of 2.2.1 -- AFFECTED
- **RHTPA 2.2.3** (build v0.4.11): ships quinn-proto 0.11.14 -- NOT AFFECTED (fixed)
- **RHTPA 2.2.4** (build v0.4.12): ships quinn-proto 0.11.14 -- NOT AFFECTED (fixed)

## Proposed Jira Update

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-id>"},
    {"id": "<RHTPA-2.2.1-jira-id>"},
    {"id": "<RHTPA-2.2.2-jira-id>"}
  ]
})
```

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (not hardcoded).

## Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

RHTPA 2.0.0 does not correspond to a configured version stream.
Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14
(the fixed version).
```
