# Step 3 -- Affects Versions Correction

## Current vs Proposed Affects Versions

Since TC-8004 is **unscoped** (no stream suffix), the Affects Versions should include all affected versions across all streams, based on lock file evidence.

### Current Affects Versions (PSIRT-assigned)

- RHTPA 2.1.0
- RHTPA 2.2.0

### Version Impact Evidence

| Version | h2 version | Affected? |
|---------|------------|-----------|
| RHTPA 2.1.0 | 0.4.5 | YES -- should be in Affects Versions |
| RHTPA 2.1.1 | 0.4.5 | YES -- should be in Affects Versions |
| RHTPA 2.2.0 | 0.4.8 | NO -- should NOT be in Affects Versions |
| RHTPA 2.2.1 | 0.4.8 | NO |
| RHTPA 2.2.2 | -- | NO (retag of 2.2.1) |
| RHTPA 2.2.3 | 0.4.9 | NO |
| RHTPA 2.2.4 | 0.4.9 | NO |

### Proposed Correction

```
Current:  [RHTPA 2.1.0, RHTPA 2.2.0]
Proposed: [RHTPA 2.1.0, RHTPA 2.1.1]
```

**Changes:**
- **Add**: RHTPA 2.1.1 (h2 0.4.5, which is < 0.4.8 -- affected)
- **Remove**: RHTPA 2.2.0 (h2 0.4.8, which is >= 0.4.8 -- not affected)

### Rationale

Lock file analysis at pinned commits from the supportability matrix shows:
- v0.3.8 (RHTPA 2.1.0): h2 0.4.5 -- within vulnerable range (< 0.4.8)
- v0.3.12 (RHTPA 2.1.1): h2 0.4.5 -- within vulnerable range (< 0.4.8)
- v0.4.5 (RHTPA 2.2.0): h2 0.4.8 -- at the fixed version, NOT vulnerable

PSIRT incorrectly included RHTPA 2.2.0 (which ships the fixed h2 0.4.8) and missed RHTPA 2.1.1 (which ships the vulnerable h2 0.4.5).

### Proposed Jira Mutation (requires engineer confirmation)

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"name": "RHTPA 2.1.0"},
    {"name": "RHTPA 2.1.1"}
  ]
})
```

Note: Actual Jira version IDs must be discovered dynamically via `getJiraIssueTypeMetaWithFields` before execution. The names above are used for clarity.

### Proposed Comment

```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
Based on lock file analysis at pinned commits from security-matrix.md.
RHTPA 2.2.0 removed (ships h2 0.4.8, at fixed version).
RHTPA 2.1.1 added (ships h2 0.4.5, within vulnerable range < 0.4.8).
Issue is unscoped -- correction applied across all streams.
```
