# Step 3 -- Affects Versions Correction: TC-8004

## Current vs Proposed Affects Versions

Since TC-8004 is **unscoped** (no stream suffix), the Affects Versions should include all actually affected versions across all streams.

| | Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.1.0, RHTPA 2.2.0 |
| **Proposed (lock file evidence)** | RHTPA 2.1.0, RHTPA 2.1.1 |

### Changes

- **Remove** RHTPA 2.2.0 -- not affected. Lock file at tag v0.4.5 shows h2 0.4.8, which is the fixed version (>= 0.4.8). PSIRT incorrectly included this version.
- **Add** RHTPA 2.1.1 -- affected. Lock file at tag v0.3.12 shows h2 0.4.5, which is within the vulnerable range (< 0.4.8). PSIRT missed this version.

### Evidence

| Version | h2 version | In affected range (< 0.4.8)? | Include in Affects Versions? |
|---------|------------|-------------------------------|------------------------------|
| RHTPA 2.1.0 | 0.4.5 | YES | YES |
| RHTPA 2.1.1 | 0.4.5 | YES | YES |
| RHTPA 2.2.0 | 0.4.8 | NO | NO |
| RHTPA 2.2.1 | 0.4.8 | NO | NO |
| RHTPA 2.2.2 | -- (retag of 2.2.1) | NO | NO |
| RHTPA 2.2.3 | 0.4.9 | NO | NO |
| RHTPA 2.2.4 | 0.4.9 | NO | NO |

### Jira Mutation (proposed)

```
jira.edit_issue("TC-8004", fields={
  "versions": [{"name": "RHTPA 2.1.0"}, {"name": "RHTPA 2.1.1"}]
})
```

Note: In a live triage, Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` and used instead of names.

### Comment (proposed)

```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].

Removed RHTPA 2.2.0: lock file at v0.4.5 shows h2 0.4.8 (fixed version, not affected).
Added RHTPA 2.1.1: lock file at v0.3.12 shows h2 0.4.5 (< 0.4.8, affected).

Based on lock file analysis at pinned commits from security-matrix.md.
Issue is unscoped -- all streams analyzed.
```
