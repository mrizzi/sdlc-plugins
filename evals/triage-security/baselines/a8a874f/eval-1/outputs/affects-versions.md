# Step 3: Affects Versions Correction

## Current vs. Proposed Affects Versions

| | Affects Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.0.0 |
| **Proposed (lock-file-verified)** | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

- **RHTPA 2.0.0 is incorrect**: This version does not correspond to any version in the supportability matrix. The matrix contains versions 2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2, 2.2.3, and 2.2.4. RHTPA 2.0.0 should be removed.
- **Stream scoping**: The issue summary tag `[rhtpa-2.2]` scopes this CVE to the **2.2.x stream only**. Although versions 2.1.0 and 2.1.1 in the 2.1.x stream also ship affected quinn-proto versions, they are out of scope for this triage.
- **Affected in 2.2.x stream**: Versions 2.2.0, 2.2.1, and 2.2.2 all ship quinn-proto < 0.11.14 and are therefore affected.
- **Not affected**: Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are excluded from Affects Versions.

## Proposed Jira Mutation

The following mutation would be executed after engineer confirmation:

### Remove incorrect version

- Remove **RHTPA 2.0.0** from Affects Versions on TC-8001

### Add verified versions

- Add **RHTPA 2.2.0** (Jira version ID: `<RHTPA-2.2.0-jira-id>`) to Affects Versions on TC-8001
- Add **RHTPA 2.2.1** (Jira version ID: `<RHTPA-2.2.1-jira-id>`) to Affects Versions on TC-8001
- Add **RHTPA 2.2.2** (Jira version ID: `<RHTPA-2.2.2-jira-id>`) to Affects Versions on TC-8001

### Jira Version ID Discovery

The placeholder IDs above (`<RHTPA-2.2.0-jira-id>`, etc.) would be discovered dynamically at execution time by calling `getJiraIssueTypeMetaWithFields` to retrieve the list of available Jira versions and matching them by name (e.g., "RHTPA 2.2.0").

### Execution Note

This is a **proposal only**. The Affects Versions update would be executed after engineer confirmation via the Jira API `editJiraIssue` operation on TC-8001.
