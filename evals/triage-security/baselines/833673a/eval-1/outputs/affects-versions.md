# Step 3 - Affects Versions Correction: TC-8001

## Current vs Proposed Affects Versions

This issue is scoped to stream **2.2.x** (from summary suffix `[rhtpa-2.2]`).
Only versions belonging to the 2.2.x stream are included in the correction.

### PSIRT-assigned (current)

- RHTPA 2.0.0

### Version impact analysis (2.2.x stream only)

| Version | Affected? | Include in Affects Versions? |
|---------|-----------|------------------------------|
| 2.2.0 | YES | YES |
| 2.2.1 | YES | YES |
| 2.2.2 | YES | YES (retag of 2.2.1, still ships vulnerable version) |
| 2.2.3 | NO | NO (ships quinn-proto 0.11.14, the fixed version) |
| 2.2.4 | NO | NO (ships quinn-proto 0.11.14, the fixed version) |

### Correction

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

**Rationale**: PSIRT assigned "RHTPA 2.0.0" which does not correspond to any version in the supportability matrix. Lock file analysis at pinned commits from security-matrix.md confirms that versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream ship quinn-proto < 0.11.14 and are affected. Versions 2.2.3 and 2.2.4 ship the fixed version (0.11.14) and are not affected.

### Jira mutation (would execute after engineer confirmation)

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-id>"},
    {"id": "<RHTPA-2.2.1-jira-id>"},
    {"id": "<RHTPA-2.2.2-jira-id>"}
  ]
})
```

Note: Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1). No hardcoded IDs are used.

### Comment (would be posted after engineer confirmation)

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

Evidence:
- 2.2.0 (v0.4.5): quinn-proto 0.11.9 (affected)
- 2.2.1 (v0.4.8): quinn-proto 0.11.12 (affected)
- 2.2.2 (v0.4.9): retag of v0.4.8, quinn-proto 0.11.12 (affected)
- 2.2.3 (v0.4.11): quinn-proto 0.11.14 (not affected - fixed version)
- 2.2.4 (v0.4.12): quinn-proto 0.11.14 (not affected - fixed version)
```

### Cross-stream note

Versions in the 2.1.x stream (2.1.0, 2.1.1) are also affected but belong to a different stream. They are not included in this issue's Affects Versions. A cross-stream impact comment would be posted to TC-8001 noting that the 2.1.x stream is also affected and should be tracked by a companion PSIRT issue.
