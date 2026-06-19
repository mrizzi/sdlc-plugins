# Step 3 -- Affects Versions Correction

## Current State (PSIRT-assigned)

The PSIRT-assigned Affects Versions on TC-8001:

| Affects Version | Correct? |
|-----------------|----------|
| RHTPA 2.0.0 | **INCORRECT** -- version 2.0.0 does not exist in any configured version stream |

## Lock-File-Verified Affected Versions

Based on the version impact analysis in Step 2, the following versions within the 2.2.x stream are confirmed affected by CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| RHTPA 2.2.0 | 0.11.9 | YES |
| RHTPA 2.2.1 | 0.11.12 | YES |
| RHTPA 2.2.2 | 0.11.12 (retag of 2.2.1) | YES |
| RHTPA 2.2.3 | 0.11.14 | NO |
| RHTPA 2.2.4 | 0.11.14 | NO |

## Proposed Correction

**Action**: Replace PSIRT-assigned Affects Versions with lock-file-verified versions.

Version names reference the Jira version prefix `RHTPA` combined with version numbers from the supportability matrix. Actual Jira version IDs would be discovered dynamically at runtime via `getJiraIssueTypeMetaWithFields` (per the skill rule: "Use dynamic version discovery. Never hardcode Jira version IDs.").

### Diff

```diff
  Affects Versions:
-   RHTPA 2.0.0
+   RHTPA 2.2.0
+   RHTPA 2.2.1
+   RHTPA 2.2.2
```

### Rationale

- **RHTPA 2.0.0 removed**: This version does not exist in any configured version stream (2.1.x or 2.2.x). It appears to be a PSIRT data entry error or an artifact of scan-time version assignment.
- **RHTPA 2.2.0 added**: Ships quinn-proto 0.11.9 (< 0.11.14) -- confirmed affected.
- **RHTPA 2.2.1 added**: Ships quinn-proto 0.11.12 (< 0.11.14) -- confirmed affected.
- **RHTPA 2.2.2 added**: Retag of 2.2.1, ships identical quinn-proto 0.11.12 -- confirmed affected.
- **RHTPA 2.2.3 NOT added**: Ships quinn-proto 0.11.14 (>= fixed version) -- not affected.
- **RHTPA 2.2.4 NOT added**: Ships quinn-proto 0.11.14 (>= fixed version) -- not affected.

## Proposed Jira Mutation

This is a proposed action pending engineer confirmation. The actual Jira update would be:

```
jira.edit_issue(
  id: "TC-8001",
  fields: {
    "versions": [
      { "name": "RHTPA 2.2.0" },
      { "name": "RHTPA 2.2.1" },
      { "name": "RHTPA 2.2.2" }
    ]
  }
)
```

Note: Jira version IDs are not hardcoded here. At runtime, the skill would first call `getJiraIssueTypeMetaWithFields` to discover the available Jira versions and their IDs, then match by version name (e.g., `RHTPA 2.2.0`) to obtain the correct ID for the API call.
