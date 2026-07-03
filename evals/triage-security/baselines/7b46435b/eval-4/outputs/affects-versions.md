# Affects Versions Correction — TC-8004

## Current vs Proposed

| | Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.1.0, RHTPA 2.2.0 |
| **Proposed (lock file evidence)** | RHTPA 2.1.0, RHTPA 2.1.1 |

## Correction Details

The PSIRT-assigned Affects Versions are **incorrect**:

1. **RHTPA 2.2.0 should be REMOVED**: Version 2.2.0 (build v0.4.5) ships h2 0.4.8, which is the fixed version. It is not affected by CVE-2026-33501. No versions in the 2.2.x stream are affected.

2. **RHTPA 2.1.1 should be ADDED**: Version 2.1.1 (build v0.3.12) ships h2 0.4.5, which is within the vulnerable range (< 0.4.8). This version is affected but was not included in the PSIRT-assigned Affects Versions.

## Scoping

Since TC-8004 is **unscoped** (no stream suffix in the summary), the Affects Versions correction includes all actually affected versions across all streams. Only the 2.1.x stream versions are affected:

- RHTPA 2.1.0 -- h2 0.4.5 (VULNERABLE)
- RHTPA 2.1.1 -- h2 0.4.5 (VULNERABLE)

The 2.2.x stream is entirely unaffected (all versions ship h2 >= 0.4.8).

## Evidence

| Version | Build Tag | h2 version | Fix threshold | Affected? |
|---------|-----------|------------|---------------|-----------|
| RHTPA 2.1.0 | v0.3.8 | 0.4.5 | 0.4.8 | YES -- include |
| RHTPA 2.1.1 | v0.3.12 | 0.4.5 | 0.4.8 | YES -- include |
| RHTPA 2.2.0 | v0.4.5 | 0.4.8 | 0.4.8 | NO -- remove |
| RHTPA 2.2.1 | v0.4.8 | 0.4.8 | 0.4.8 | NO |
| RHTPA 2.2.2 | v0.4.9 | (retag) | 0.4.8 | NO |
| RHTPA 2.2.3 | v0.4.11 | 0.4.9 | 0.4.8 | NO |
| RHTPA 2.2.4 | v0.4.12 | 0.4.9 | 0.4.8 | NO |

## Proposed Jira Mutation

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"name": "RHTPA 2.1.0"},
    {"name": "RHTPA 2.1.1"}
  ]
})
```

Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to all affected versions (unscoped issue -- all streams analyzed).
