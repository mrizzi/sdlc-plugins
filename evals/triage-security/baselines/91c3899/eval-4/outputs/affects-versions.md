# Step 3 -- Affects Versions Correction: TC-8004

## Current Affects Versions (PSIRT-assigned)

The Vulnerability issue TC-8004 currently has the following Affects Versions set by PSIRT:

- RHTPA 2.1.0
- RHTPA 2.2.0

## Version Impact Evidence

Based on the lock file analysis in Step 2:

| Version | h2 Version | Affected? |
|---------|------------|-----------|
| RHTPA 2.1.0 | 0.4.5 | **YES** -- within vulnerable range (< 0.4.8) |
| RHTPA 2.1.1 | 0.4.5 | **YES** -- within vulnerable range (< 0.4.8) |
| RHTPA 2.2.0 | 0.4.8 | **NO** -- ships the fixed version (>= 0.4.8) |
| RHTPA 2.2.1 | 0.4.8 | **NO** -- ships the fixed version (>= 0.4.8) |
| RHTPA 2.2.2 | (retag of 2.2.1) | **NO** -- same as 2.2.1 |
| RHTPA 2.2.3 | 0.4.9 | **NO** -- ships version past the fix |
| RHTPA 2.2.4 | 0.4.9 | **NO** -- ships version past the fix |

## Correction Required

The PSIRT-assigned Affects Versions are **incorrect**. PSIRT included RHTPA 2.2.0, but lock file evidence shows that version ships h2 0.4.8 (the fixed version) and is NOT affected. Additionally, RHTPA 2.1.1 is missing from the Affects Versions but IS affected.

### Changes

| Action | Version | Reason |
|--------|---------|--------|
| **KEEP** | RHTPA 2.1.0 | Correctly identified as affected -- ships h2 0.4.5 (< 0.4.8) |
| **ADD** | RHTPA 2.1.1 | Missing from PSIRT assignment -- ships h2 0.4.5 (< 0.4.8), confirmed affected |
| **REMOVE** | RHTPA 2.2.0 | Incorrectly included by PSIRT -- ships h2 0.4.8, not affected |

### Corrected Affects Versions

The Affects Versions field should be updated to include **only** the actually affected versions:

- **RHTPA 2.1.0**
- **RHTPA 2.1.1**

These are the only versions that ship h2 < 0.4.8 (the vulnerable range). All 2.2.x versions ship h2 >= 0.4.8 and are not affected.

## Scope Note

Since this issue is **unscoped** (no stream suffix), the Affects Versions correction covers all streams. The corrected list includes only 2.1.x versions because those are the only versions where h2 falls within the vulnerable range.

## Proposed Jira Update

```
jira.edit_issue(
  id: "TC-8004",
  fields: {
    "versions": [
      { "name": "RHTPA 2.1.0" },
      { "name": "RHTPA 2.1.1" }
    ]
  }
)
```

This update requires engineer confirmation before execution.
