# Step 3 -- Affects Versions Correction: TC-8004

## Current vs Corrected Affects Versions

| | Versions |
|---|---|
| PSIRT-assigned (current) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Lock-file-verified (corrected) | RHTPA 2.1.0, RHTPA 2.1.1 |

## Correction Details

### Versions to REMOVE

| Version | Reason |
|---------|--------|
| RHTPA 2.2.0 | h2 0.4.8 shipped at build tag v0.4.5 -- this is the fix threshold version (>= 0.4.8), so 2.2.0 is NOT affected |

### Versions to ADD

| Version | Reason |
|---------|--------|
| RHTPA 2.1.1 | h2 0.4.5 shipped at build tag v0.3.12 -- this is below the fix threshold (< 0.4.8), so 2.1.1 IS affected |

### Versions to KEEP

| Version | Reason |
|---------|--------|
| RHTPA 2.1.0 | h2 0.4.5 shipped at build tag v0.3.8 -- correctly identified as affected by PSIRT |

## Rationale

PSIRT assigned Affects Versions based on scan time, listing RHTPA 2.1.0 and RHTPA 2.2.0. Lock file analysis at pinned source commits reveals:

1. **RHTPA 2.2.0 is NOT affected**: The build tag v0.4.5 for version 2.2.0 ships h2 0.4.8, which is the exact fix threshold. The CVE description states "versions before 0.4.8" are vulnerable, meaning 0.4.8 itself is the fixed version and is not vulnerable.

2. **RHTPA 2.1.1 IS affected but was missing**: The build tag v0.3.12 for version 2.1.1 ships h2 0.4.5, which is below the fix threshold. PSIRT did not include this version in Affects Versions.

The corrected Affects Versions should be: **RHTPA 2.1.0, RHTPA 2.1.1** -- scoped to only the versions in the 2.1.x stream that actually ship the vulnerable h2 dependency.

## Proposed Jira Update

```
jira.edit_issue("TC-8004", fields: {
  "versions": [
    { "name": "RHTPA 2.1.0" },
    { "name": "RHTPA 2.1.1" }
  ]
})
```

Note: Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` in a live triage. The names above are illustrative.

## Affects Versions Correction Comment

The following comment would be posted to TC-8004 after engineer confirmation:

```
Affects Versions corrected based on lock file analysis:
- Removed: RHTPA 2.2.0 (ships h2 0.4.8, which is the fixed version)
- Added: RHTPA 2.1.1 (ships h2 0.4.5, below fix threshold 0.4.8)
- Kept: RHTPA 2.1.0 (ships h2 0.4.5, confirmed affected)

Evidence: Cargo.lock at pinned source commits in security-matrix.md.
```
