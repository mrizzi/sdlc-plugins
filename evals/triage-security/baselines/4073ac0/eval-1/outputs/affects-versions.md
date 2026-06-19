# Step 3 -- Affects Versions Correction

## Current vs Proposed

The PSIRT-assigned Affects Versions is incorrect. `RHTPA 2.0.0` does not exist as a configured version stream -- there is no 2.0.x stream in the Version Streams table.

Since this issue is scoped to stream **2.2.x** (per the summary suffix `[rhtpa-2.2]`), only 2.2.x versions that are affected should be included. Based on the version impact table:

- 2.2.0: quinn-proto 0.11.9 -- AFFECTED
- 2.2.1: quinn-proto 0.11.12 -- AFFECTED
- 2.2.2: quinn-proto 0.11.12 (retag of 2.2.1) -- AFFECTED
- 2.2.3: quinn-proto 0.11.14 -- NOT affected (ships fixed version)
- 2.2.4: quinn-proto 0.11.14 -- NOT affected (ships fixed version)

## PROPOSED Correction

```
Current Affects Versions:  [RHTPA 2.0.0]
Proposed Affects Versions: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

**Rationale**: PSIRT assigned `RHTPA 2.0.0` which does not correspond to any supported version stream. Lock file analysis at pinned commits from the supportability matrix confirms that versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto < 0.11.14 (the vulnerable range). Versions 2.2.3 and 2.2.4 ship the fixed version (0.11.14) and are not affected. Correction is scoped to the 2.2.x stream per the issue suffix `[rhtpa-2.2]`.

## PROPOSED Jira Mutation (requires engineer confirmation)

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-id>"},
    {"id": "<RHTPA-2.2.1-jira-id>"},
    {"id": "<RHTPA-2.2.2-jira-id>"}
  ]
})
```

Note: Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` -- not hardcoded.

## PROPOSED Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on Cargo.lock analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

- RHTPA 2.2.0 (tag v0.4.5): quinn-proto 0.11.9 -- vulnerable
- RHTPA 2.2.1 (tag v0.4.8): quinn-proto 0.11.12 -- vulnerable
- RHTPA 2.2.2 (tag v0.4.8): retag of 2.2.1 -- vulnerable (same as 2.2.1)
- RHTPA 2.2.3 (tag v0.4.11): quinn-proto 0.11.14 -- not affected (fixed version)
- RHTPA 2.2.4 (tag v0.4.12): quinn-proto 0.11.14 -- not affected (fixed version)
```

## Cross-Stream Note

The 2.1.x stream is also affected (versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9) but is outside the scope of this issue. A companion PSIRT issue for the 2.1.x stream would need separate triage, or a cross-stream impact comment should be posted to TC-8001.
