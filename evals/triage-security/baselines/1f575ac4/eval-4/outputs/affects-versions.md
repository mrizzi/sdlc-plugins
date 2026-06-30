# Affects Versions Correction — TC-8004

## Current vs Proposed

| | Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.1.0, RHTPA 2.2.0 |
| **Proposed (lock file evidence)** | RHTPA 2.1.0, RHTPA 2.1.1 |

## Correction Details

The PSIRT-assigned Affects Versions are **incorrect**:

1. **RHTPA 2.2.0 should be removed**: Lock file analysis shows h2 0.4.8 at tag v0.4.5 (build for version 2.2.0), which is at or above the fix threshold (>= 0.4.8). Version 2.2.0 is NOT affected.

2. **RHTPA 2.1.1 should be added**: Lock file analysis shows h2 0.4.5 at tag v0.3.12 (build for version 2.1.1), which is below the fix threshold. Version 2.1.1 IS affected but was not included by PSIRT.

## Scope

Since TC-8004 is **unscoped** (no stream suffix in the summary), the Affects Versions correction includes all affected versions across all streams. The lock file evidence shows:

- **2.1.x stream**: Both 2.1.0 and 2.1.1 ship h2 0.4.5 (vulnerable) — both should be listed
- **2.2.x stream**: All versions ship h2 >= 0.4.8 (fixed) — none should be listed

## Evidence

| Version | Build Tag | h2 Version | Fix Threshold | Affected? |
|---------|-----------|------------|---------------|-----------|
| RHTPA 2.1.0 | v0.3.8 | 0.4.5 | 0.4.8 | YES — include |
| RHTPA 2.1.1 | v0.3.12 | 0.4.5 | 0.4.8 | YES — include |
| RHTPA 2.2.0 | v0.4.5 | 0.4.8 | 0.4.8 | NO — remove |
| RHTPA 2.2.1 | v0.4.8 | 0.4.8 | 0.4.8 | NO — not included |
| RHTPA 2.2.2 | v0.4.9 | (retag) | 0.4.8 | NO — not included |
| RHTPA 2.2.3 | v0.4.11 | 0.4.9 | 0.4.8 | NO — not included |
| RHTPA 2.2.4 | v0.4.12 | 0.4.9 | 0.4.8 | NO — not included |

## Proposed Jira Update

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"name": "RHTPA 2.1.0"},
    {"name": "RHTPA 2.1.1"}
  ]
})
```

## Comment

```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].

Based on lock file analysis at pinned commits from security-matrix.md:
- RHTPA 2.2.0 removed: ships h2 0.4.8 (at fix threshold, not affected)
- RHTPA 2.1.1 added: ships h2 0.4.5 (below fix threshold 0.4.8, affected)

This is an unscoped issue — Affects Versions include all affected versions across all streams.
Only the 2.1.x stream is affected; the 2.2.x stream ships the patched version.
```
