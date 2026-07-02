# Step 3 -- Affects Versions Correction

## Current vs Proposed Affects Versions

Since TC-8004 is **unscoped** (no stream suffix), the Affects Versions correction includes all affected versions across all streams.

| | Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.1.0, RHTPA 2.2.0 |
| **Proposed (lock file evidence)** | RHTPA 2.1.0, RHTPA 2.1.1 |

## Correction Details

- **RHTPA 2.1.0** -- KEEP. Lock file evidence confirms h2 0.4.5 (vulnerable, below fix threshold 0.4.8).
- **RHTPA 2.1.1** -- ADD. Lock file evidence confirms h2 0.4.5 (vulnerable). PSIRT missed this version.
- **RHTPA 2.2.0** -- REMOVE. Lock file evidence confirms h2 0.4.8 (fixed version). Not affected.

All 2.2.x versions (2.2.0 through 2.2.4) ship h2 >= 0.4.8 and are **not affected**. The PSIRT-assigned RHTPA 2.2.0 is incorrect and should be removed.

## Rationale

The correction is scoped to actually affected versions only, based on lock file analysis at pinned commits from security-matrix.md:

- `git show v0.3.8:Cargo.lock` -- h2 = 0.4.5 (AFFECTED) -- maps to RHTPA 2.1.0
- `git show v0.3.12:Cargo.lock` -- h2 = 0.4.5 (AFFECTED) -- maps to RHTPA 2.1.1
- `git show v0.4.5:Cargo.lock` -- h2 = 0.4.8 (NOT AFFECTED) -- maps to RHTPA 2.2.0

## Proposed Jira Update

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"name": "RHTPA 2.1.0"},
    {"name": "RHTPA 2.1.1"}
  ]
})
```

Comment to be posted on TC-8004:

> Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
> Based on lock file analysis at pinned commits from security-matrix.md.
> RHTPA 2.2.0 removed -- ships h2 0.4.8 (fixed version, not affected).
> RHTPA 2.1.1 added -- ships h2 0.4.5 (vulnerable, below fix threshold 0.4.8).
> Issue is unscoped (no stream suffix) -- correction covers all streams.
