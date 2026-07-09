# Affects Versions Correction — TC-8001

## Step 3 — Affects Versions Correction

### Stream scope

This issue is scoped to stream **2.2.x** (from summary suffix `[rhtpa-2.2]`).
Only versions belonging to the 2.2.x stream are included in the Affects Versions
correction. The 2.1.x versions (2.1.0, 2.1.1) are affected but belong to a
companion/sibling issue scope.

### Current vs Proposed

```
Current Affects Versions:  [RHTPA 2.0.0]
Proposed Affects Versions: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

### Rationale

- **RHTPA 2.0.0** is incorrect: there is no version 2.0.0 in either the 2.1.x or
  2.2.x supportability matrix. PSIRT likely assigned this based on scan-time
  metadata rather than actual dependency analysis.
- **RHTPA 2.2.0** (build v0.4.5): ships quinn-proto 0.11.9, which is < 0.11.14 (AFFECTED)
- **RHTPA 2.2.1** (build v0.4.8): ships quinn-proto 0.11.12, which is < 0.11.14 (AFFECTED)
- **RHTPA 2.2.2** (build v0.4.9): retag of 2.2.1, same quinn-proto 0.11.12 (AFFECTED)
- **RHTPA 2.2.3** (build v0.4.11): ships quinn-proto 0.11.14, which is the fixed version (NOT AFFECTED)
- **RHTPA 2.2.4** (build v0.4.12): ships quinn-proto 0.11.14 (NOT AFFECTED)

### Proposed Jira mutation (requires engineer confirmation)

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
(not hardcoded).

### Proposed comment on TC-8001

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

Evidence:
- RHTPA 2.2.0 (v0.4.5): quinn-proto 0.11.9 (affected)
- RHTPA 2.2.1 (v0.4.8): quinn-proto 0.11.12 (affected)
- RHTPA 2.2.2 (v0.4.9): retag of 2.2.1 (affected)
- RHTPA 2.2.3 (v0.4.11): quinn-proto 0.11.14 (fixed - not included)
- RHTPA 2.2.4 (v0.4.12): quinn-proto 0.11.14 (fixed - not included)
```
