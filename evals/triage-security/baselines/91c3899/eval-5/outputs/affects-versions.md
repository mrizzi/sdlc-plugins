# Step 3 -- Affects Versions Correction

## Current Affects Versions (from Jira)

The Vulnerability issue TC-8005 currently has:

- **Affects Versions**: RHTPA 2.0.0

## Version Impact Evidence (from Step 2)

Based on rpms.lock.yaml inspection across the 2.2.x stream:

| Version | openssl-libs | Affected? |
|---------|--------------|-----------|
| 2.2.0 | 3.0.7-25.el9_3 | YES |
| 2.2.1 | 3.0.7-27.el9_4 | YES |
| 2.2.2 | 3.0.7-27.el9_4 | YES |
| 2.2.3 | 3.0.7-28.el9_4 | NO |
| 2.2.4 | 3.0.7-28.el9_4 | NO |

## Correction Required

The PSIRT-assigned Affects Versions is **incorrect**. The issue currently lists `RHTPA 2.0.0`, but:

1. There is no `2.0.x` version stream configured -- `RHTPA 2.0.0` does not correspond to any supported stream
2. The issue is scoped to the `2.2.x` stream (per summary suffix `[rhtpa-2.2]`)
3. Lock file evidence shows versions **2.2.0, 2.2.1, and 2.2.2** are affected

### Proposed Affects Versions Update

**Remove**: RHTPA 2.0.0 (incorrect -- no evidence of this version being affected, and no 2.0.x stream is configured)

**Add**:
- RHTPA 2.2.0
- RHTPA 2.2.1
- RHTPA 2.2.2

These three versions ship openssl-libs at versions below the fixed 3.0.7-28.el9_4.

**Do NOT add**:
- RHTPA 2.2.3 (ships 3.0.7-28.el9_4 -- the fixed version)
- RHTPA 2.2.4 (ships 3.0.7-28.el9_4 -- the fixed version)

### Jira API Call (pending engineer confirmation)

```
jira.edit_issue("TC-8005", {
  "versions": [
    {"name": "RHTPA 2.2.0"},
    {"name": "RHTPA 2.2.1"},
    {"name": "RHTPA 2.2.2"}
  ]
})
```

Note: The actual Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` -- never hardcoded. The version names above are illustrative; the actual API call uses the IDs returned by Jira's metadata endpoint.
