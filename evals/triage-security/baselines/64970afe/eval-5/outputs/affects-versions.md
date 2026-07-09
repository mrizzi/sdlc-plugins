# Step 3 -- Affects Versions Correction

## Current Affects Versions (PSIRT-assigned)

- RHTPA 2.0.0

## Lock File Evidence (2.2.x stream -- issue scope)

| Version | openssl-libs | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 3.0.7-25.el9_3 | YES |
| 2.2.1 | 3.0.7-27.el9_4 | YES |
| 2.2.2 | (retag of 2.2.1) | YES |
| 2.2.3 | 3.0.7-28.el9_4 | NO |
| 2.2.4 | 3.0.7-28.el9_4 | NO |

## Correction Required

The PSIRT-assigned Affects Versions value of "RHTPA 2.0.0" is **incorrect**. There is no 2.0.x stream configured in the Version Streams table, and the issue is scoped to the 2.2.x stream based on the `[rhtpa-2.2]` suffix.

### Proposed Affects Versions

**Remove:**
- RHTPA 2.0.0 (no such stream configured; not supported)

**Add:**
- RHTPA 2.2.0
- RHTPA 2.2.1
- RHTPA 2.2.2

These are the versions within the 2.2.x stream (the issue's scope) that ship openssl-libs versions below the fix threshold of 3.0.7-28.el9_4. Versions 2.2.3 and 2.2.4 are excluded because they already ship the fixed version.

### Rationale

PSIRT assigns Affects Versions based on scan time and component presence, not actual dependency version analysis. The rpms.lock.yaml inspection at each pinned tag confirms that only versions 2.2.0 through 2.2.2 ship a vulnerable openssl-libs. Version 2.0.0 does not exist in any configured version stream.

### Jira Update (would execute)

```
jira.edit_issue("TC-8005", {
  "versions": [
    {"name": "RHTPA 2.2.0"},
    {"name": "RHTPA 2.2.1"},
    {"name": "RHTPA 2.2.2"}
  ]
})
```

Note: In a live triage, version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` rather than using hardcoded names.
