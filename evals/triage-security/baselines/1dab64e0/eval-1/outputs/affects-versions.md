# Step 3 -- Affects Versions Correction

## Current State

The Jira issue TC-8001 currently has:
- **Affects Versions**: RHTPA 2.0.0

## Problem

The current Affects Versions value is incorrect for two reasons:

1. **RHTPA 2.0.0 does not correspond to any configured version stream.** The Security Configuration defines streams 2.1.x and 2.2.x -- there is no 2.0.x stream. PSIRT assigned this version based on scan time, not actual dependency analysis.

2. **The issue is scoped to the 2.2.x stream** (from the summary suffix `[rhtpa-2.2]`). The version impact analysis shows that within the 2.2.x stream, versions 2.2.0, 2.2.1, and 2.2.2 are affected, while 2.2.3 and 2.2.4 are not affected (they ship quinn-proto 0.11.14, which is the fixed version).

## Proposed Correction

**Remove**: RHTPA 2.0.0

**Add**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

The corrected Affects Versions field should contain only the versions within the scoped stream (2.2.x) that are actually affected based on lock file evidence:

| Version | quinn-proto | Affected? | In Affects Versions? |
|---------|-------------|-----------|----------------------|
| RHTPA 2.0.0 | N/A (no stream) | N/A | REMOVE |
| RHTPA 2.2.0 | 0.11.9 | YES | ADD |
| RHTPA 2.2.1 | 0.11.12 | YES | ADD |
| RHTPA 2.2.2 | 0.11.12 | YES (retag of 2.2.1) | ADD |
| RHTPA 2.2.3 | 0.11.14 | NO (fixed) | -- |
| RHTPA 2.2.4 | 0.11.14 | NO (fixed) | -- |

Note: Versions 2.1.0 and 2.1.1 (from the 2.1.x stream) are also affected but are NOT included in the Affects Versions correction because this issue is scoped to the 2.2.x stream. Cross-stream impact is handled in Step 8 Case B.

## Proposed Jira Mutation

```
jira.edit_issue("TC-8001", versions=["RHTPA 2.2.0", "RHTPA 2.2.1", "RHTPA 2.2.2"])
```

This requires dynamic version discovery via `getJiraIssueTypeMetaWithFields` to find the Jira version IDs for RHTPA 2.2.0, RHTPA 2.2.1, and RHTPA 2.2.2. The version IDs must not be hardcoded.

A Jira comment documenting the correction would be posted:

> Affects Versions corrected based on lock file analysis:
>
> Removed: RHTPA 2.0.0 (no corresponding version stream configured)
> Added: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
>
> Evidence: quinn-proto versions at pinned commits show 0.11.9 (2.2.0) and 0.11.12 (2.2.1, 2.2.2) -- both below the fix threshold of 0.11.14. Versions 2.2.3+ ship quinn-proto 0.11.14 (fixed).
> Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
