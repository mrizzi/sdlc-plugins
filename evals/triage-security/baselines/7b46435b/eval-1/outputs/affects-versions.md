# Step 3 -- Affects Versions Correction

## Current vs Proposed

The issue TC-8001 is scoped to stream **2.2.x** (from the `[rhtpa-2.2]` suffix). Only versions belonging to the 2.2.x stream are included in the Affects Versions correction. The 2.1.x versions (also affected) belong to a companion/sibling issue for the 2.1.x stream.

| | Affects Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.0.0 |
| **Proposed (lock file evidence)** | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

- **RHTPA 2.0.0** is incorrect -- there is no 2.0.x version stream configured. PSIRT likely assigned this based on scan time rather than actual dependency analysis.
- **RHTPA 2.2.0** -- ships quinn-proto 0.11.9 (vulnerable, < 0.11.14). Confirmed via `git show v0.4.5:Cargo.lock`.
- **RHTPA 2.2.1** -- ships quinn-proto 0.11.12 (vulnerable, < 0.11.14). Confirmed via `git show v0.4.8:Cargo.lock`.
- **RHTPA 2.2.2** -- retag of 2.2.1, same backend source (v0.4.8), ships quinn-proto 0.11.12 (vulnerable).
- **RHTPA 2.2.3** -- ships quinn-proto 0.11.14 (fixed version). NOT affected. Excluded.
- **RHTPA 2.2.4** -- ships quinn-proto 0.11.14 (fixed version). NOT affected. Excluded.

## Proposed Jira Update

After engineer confirmation:

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<jira-id-for-RHTPA-2.2.0>"},
    {"id": "<jira-id-for-RHTPA-2.2.1>"},
    {"id": "<jira-id-for-RHTPA-2.2.2>"}
  ]
})
```

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1).

## Correction Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

RHTPA 2.0.0 removed -- no 2.0.x version stream exists.
RHTPA 2.2.3 and 2.2.4 excluded -- ship quinn-proto 0.11.14 (fixed version).
```
