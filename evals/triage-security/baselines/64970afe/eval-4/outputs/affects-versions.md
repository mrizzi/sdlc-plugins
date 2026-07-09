# Step 3 -- Affects Versions Correction: TC-8004

## Current vs Corrected Affects Versions

| | Versions |
|---|---|
| PSIRT-claimed (current) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Corrected (based on lock file evidence) | RHTPA 2.1.0, RHTPA 2.1.1 |

## Changes Required

| Action | Version | Rationale |
|--------|---------|-----------|
| KEEP | RHTPA 2.1.0 | h2 0.4.5 at tag v0.3.8 -- below fix threshold 0.4.8; affected |
| ADD | RHTPA 2.1.1 | h2 0.4.5 at tag v0.3.12 -- below fix threshold 0.4.8; affected but missing from PSIRT list |
| REMOVE | RHTPA 2.2.0 | h2 0.4.8 at tag v0.4.5 -- equals fix threshold 0.4.8; NOT affected |

## Rationale

PSIRT assigned Affects Versions based on scan time, listing RHTPA 2.1.0 and RHTPA 2.2.0. Lock file analysis reveals:

1. **RHTPA 2.1.0** -- correctly identified as affected. The backend build tag v0.3.8 ships h2 0.4.5 which is below the fix threshold of 0.4.8.

2. **RHTPA 2.1.1** -- missing from PSIRT list but affected. The backend build tag v0.3.12 also ships h2 0.4.5 (same version as 2.1.0). This version must be added to Affects Versions.

3. **RHTPA 2.2.0** -- incorrectly listed as affected. The backend build tag v0.4.5 ships h2 0.4.8 which is the fixed version. All 2.2.x versions (2.2.0 through 2.2.4) ship h2 >= 0.4.8 and are NOT affected. RHTPA 2.2.0 must be removed from Affects Versions.

## Scoping Note

Because this is an **unscoped** issue (no stream suffix in the summary), the Affects Versions correction covers all streams. The corrected list includes only the actually affected versions from the 2.1.x stream, scoped to versions that ship the vulnerable dependency based on lock file evidence.

## Proposed Jira Mutation

```
jira.edit_issue("TC-8004", {
  "versions": [
    {"name": "RHTPA 2.1.0"},
    {"name": "RHTPA 2.1.1"}
  ]
})
```

This update removes RHTPA 2.2.0 (not affected) and adds RHTPA 2.1.1 (affected but missing).
