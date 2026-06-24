# Step 3 -- Affects Versions Correction: TC-8004

## Current vs Proposed Affects Versions

The issue is **unscoped** (no stream suffix), so the Affects Versions correction applies across all streams but must be scoped to **actually affected versions only** based on lock file evidence.

### PSIRT-assigned Affects Versions (current)

- RHTPA 2.1.0
- RHTPA 2.2.0

### Lock-file-verified Impact

From the version impact table:

| Version | h2 version | Affected? |
|---------|------------|-----------|
| RHTPA 2.1.0 | 0.4.5 | **YES** |
| RHTPA 2.1.1 | 0.4.5 | **YES** |
| RHTPA 2.2.0 | 0.4.8 | NO |
| RHTPA 2.2.1 | 0.4.8 | NO |
| RHTPA 2.2.2 | -- | NO (retag of 2.2.1) |
| RHTPA 2.2.3 | 0.4.9 | NO |
| RHTPA 2.2.4 | 0.4.9 | NO |

### Proposed Affects Versions

```
Current:  [RHTPA 2.1.0, RHTPA 2.2.0]
Proposed: [RHTPA 2.1.0, RHTPA 2.1.1]
```

### Correction Details

1. **Remove RHTPA 2.2.0**: The 2.2.x stream ships h2 0.4.8 (the fix threshold) starting from version 2.2.0. No 2.2.x versions are affected. RHTPA 2.2.0 was incorrectly assigned by PSIRT.

2. **Add RHTPA 2.1.1**: PSIRT included RHTPA 2.1.0 but missed RHTPA 2.1.1, which also ships h2 0.4.5 (vulnerable). Both 2.1.x versions are affected.

### Rationale

PSIRT assigned Affects Versions based on scan time and initial assessment, listing one version per stream (RHTPA 2.1.0 and RHTPA 2.2.0). Lock file analysis at pinned commits from the security-matrix.md reveals:

- The 2.2.x stream is **not affected** -- all versions ship h2 >= 0.4.8 (the fix threshold). RHTPA 2.2.0 should be removed.
- The 2.1.x stream is **fully affected** -- both RHTPA 2.1.0 and RHTPA 2.1.1 ship h2 0.4.5. RHTPA 2.1.1 was missing and should be added.

### Jira Update (proposed)

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"name": "RHTPA 2.1.0"},
    {"name": "RHTPA 2.1.1"}
  ]
})
```

Followed by a comment:

```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
Based on lock file analysis at pinned commits from security-matrix.md.
- Removed RHTPA 2.2.0: 2.2.x stream ships h2 0.4.8 (at/above fix threshold) -- not affected.
- Added RHTPA 2.1.1: ships h2 0.4.5 (below fix threshold of 0.4.8) -- affected.
Issue is unscoped; correction covers all streams based on actual dependency versions.
```
