# Step 3 -- Affects Versions Correction

## 3.1 -- Current Affects Versions (from Jira)

Current Affects Versions on TC-8005: **RHTPA 2.0.0**

## 3.2 -- Version Impact Analysis (scoped to 2.2.x stream)

From the version impact table, the affected versions in the 2.2.x stream are:

| Version | Affected? |
|---------|-----------|
| RHTPA 2.2.0 | YES |
| RHTPA 2.2.1 | YES |
| RHTPA 2.2.2 | YES (retag of 2.2.1) |
| RHTPA 2.2.3 | NO (ships fixed 3.0.7-28.el9_4) |
| RHTPA 2.2.4 | NO (ships fixed 3.0.7-28.el9_4) |

## 3.3 -- Correction Analysis

The PSIRT-assigned Affects Version is **wrong**:
- "RHTPA 2.0.0" does not correspond to any configured version stream (no 2.0.x stream exists in the Version Streams table).
- The issue suffix `[rhtpa-2.2]` scopes it to the 2.2.x stream.
- Lock file evidence shows versions 2.2.0, 2.2.1, and 2.2.2 are affected.

## Proposed Correction

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

**Rationale**: Based on rpms.lock.yaml analysis at pinned commits from the supportability matrix. Versions 2.2.0 (openssl-libs 3.0.7-25.el9_3), 2.2.1 (3.0.7-27.el9_4), and 2.2.2 (retag of 2.2.1) all ship openssl-libs versions before the fix threshold (3.0.7-28.el9_4). Versions 2.2.3 and 2.2.4 already ship the fixed version and are excluded. RHTPA 2.0.0 is removed because no 2.0.x stream is configured.

Scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`. The 2.1.x stream versions (also affected) are not included here -- they belong to any companion CVE Jira for the 2.1.x stream.

## Proposed Jira Mutation (requires engineer confirmation)

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

## Proposed Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

Versions 2.2.3+ already ship openssl-libs 3.0.7-28.el9_4 (the fixed version) and are not affected.
```
