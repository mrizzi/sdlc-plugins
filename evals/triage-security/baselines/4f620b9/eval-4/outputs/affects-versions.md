# Step 3 -- Affects Versions Correction

## Current Affects Versions (PSIRT-assigned)

The Vulnerability issue TC-8004 currently has:

- RHTPA 2.1.0
- RHTPA 2.2.0

## Version Impact Evidence

Based on lock file analysis in Step 2:

| Version | h2 version | Within affected range (< 0.4.8)? |
|---------|------------|-----------------------------------|
| RHTPA 2.1.0 | 0.4.5 | YES -- affected |
| RHTPA 2.1.1 | 0.4.5 | YES -- affected (missing from PSIRT assignment) |
| RHTPA 2.2.0 | 0.4.8 | NO -- ships fixed version |
| RHTPA 2.2.1 | 0.4.8 | NO -- ships fixed version |
| RHTPA 2.2.2 | (retag of 2.2.1) | NO -- ships fixed version |
| RHTPA 2.2.3 | 0.4.9 | NO -- ships fixed version |
| RHTPA 2.2.4 | 0.4.9 | NO -- ships fixed version |

## Proposed Correction

**Remove**: RHTPA 2.2.0 (ships h2 0.4.8, which is the fixed version -- not affected)

**Add**: RHTPA 2.1.1 (ships h2 0.4.5, which is within the affected range -- missing from PSIRT assignment)

**Keep**: RHTPA 2.1.0 (correctly identified as affected)

### Corrected Affects Versions

- RHTPA 2.1.0
- RHTPA 2.1.1

### Rationale

PSIRT assigned Affects Versions based on component scan coverage, which included both 2.1.0 and 2.2.0. However, lock file analysis shows that the 2.2.x stream ships h2 >= 0.4.8 (the fixed version) starting from the very first release (2.2.0). Meanwhile, RHTPA 2.1.1 was omitted despite also shipping the vulnerable h2 0.4.5.

The correction scopes Affects Versions to only the versions that actually ship the vulnerable dependency.

## Proposed Jira Mutation

**Action**: Update Affects Versions on TC-8004

```
jira.edit_issue("TC-8004", {
  "versions": [
    {"name": "RHTPA 2.1.0"},
    {"name": "RHTPA 2.1.1"}
  ]
})
```

This is a **proposal** -- requires engineer confirmation before execution.
