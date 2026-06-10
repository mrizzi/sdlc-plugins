# Step 3 -- Affects Versions Correction

## Current State

The PSIRT-assigned Affects Versions on TC-8001 is: **RHTPA 2.0.0**

This is incorrect. There is no RHTPA 2.0.0 in the supportability matrix -- PSIRT likely assigned it based on scan-time defaults rather than actual dependency analysis.

## Stream Scope

The issue is scoped to the **2.2.x stream** (per summary suffix `[rhtpa-2.2]`). Therefore, the Affects Versions correction should only include versions from the 2.2.x stream that are actually affected, per the version impact table.

## Affected Versions Within Scope (2.2.x Stream)

From the version impact analysis:

| Version | Affected? | Include in Affects Versions? |
|---------|-----------|------------------------------|
| RHTPA 2.2.0 | YES | YES |
| RHTPA 2.2.1 | YES | YES |
| RHTPA 2.2.2 | YES (retag of 2.2.1) | YES |
| RHTPA 2.2.3 | NO (ships 0.11.14) | NO |
| RHTPA 2.2.4 | NO (ships 0.11.14) | NO |

## Proposed Correction

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

**Rationale**: Lock file analysis at pinned commits from the supportability matrix confirms that RHTPA 2.2.0 (quinn-proto 0.11.9), RHTPA 2.2.1 (quinn-proto 0.11.12), and RHTPA 2.2.2 (retag of 2.2.1, same quinn-proto 0.11.12) all ship a vulnerable version of quinn-proto (< 0.11.14). RHTPA 2.0.0 does not exist in the supportability matrix and should be removed.

RHTPA 2.2.3 and RHTPA 2.2.4 are NOT included because they ship quinn-proto 0.11.14 (the fixed version).

## Cross-Stream Note

Versions from the 2.1.x stream (RHTPA 2.1.0, RHTPA 2.1.1) are also affected but are **not** included in this issue's Affects Versions because the issue is scoped to the 2.2.x stream. The 2.1.x impact should be tracked by a companion PSIRT issue for that stream (see Step 4 cross-stream coordination).

## Proposed Jira Mutation (requires engineer confirmation)

```
PROPOSAL: Update Affects Versions on TC-8001
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"name": "RHTPA 2.2.0"},
    {"name": "RHTPA 2.2.1"},
    {"name": "RHTPA 2.2.2"}
  ]
})
```

Note: Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` at runtime (Important Rule 6). Version names from the supportability matrix are used here as references.

## Proposed Comment (requires engineer confirmation)

```
PROPOSAL: Add comment to TC-8001

"Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from the supportability matrix.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

Evidence:
- RHTPA 2.2.0 (v0.4.5): quinn-proto 0.11.9 (affected)
- RHTPA 2.2.1 (v0.4.8): quinn-proto 0.11.12 (affected)
- RHTPA 2.2.2 (v0.4.9): retag of 2.2.1 (affected, same as RHTPA 2.2.1)
- RHTPA 2.2.3 (v0.4.11): quinn-proto 0.11.14 (not affected -- fixed version)
- RHTPA 2.2.4 (v0.4.12): quinn-proto 0.11.14 (not affected -- fixed version)

RHTPA 2.0.0 removed: no such version exists in the supportability matrix."
```
