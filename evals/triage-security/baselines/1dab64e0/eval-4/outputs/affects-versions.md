# Step 3 -- Affects Versions Correction

## Current vs Proposed Affects Versions

The issue is **unscoped** (no stream suffix), so the Affects Versions correction applies across all streams but is scoped to **actually affected versions only** based on lock file evidence.

| | Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.1.0, RHTPA 2.2.0 |
| **Proposed (lock file evidence)** | RHTPA 2.1.0, RHTPA 2.1.1 |

## Changes

| Action | Version | Reason |
|--------|---------|--------|
| **Keep** | RHTPA 2.1.0 | Affected -- ships h2 0.4.5 (below fix threshold 0.4.8) |
| **Add** | RHTPA 2.1.1 | Affected -- ships h2 0.4.5 (below fix threshold 0.4.8); was missing from PSIRT assignment |
| **Remove** | RHTPA 2.2.0 | Not affected -- ships h2 0.4.8 (at fix threshold); PSIRT incorrectly included this version |

## Rationale

PSIRT assigned Affects Versions based on scan-time component presence, not actual dependency version analysis. Lock file inspection at pinned source commits from security-matrix.md reveals:

- **RHTPA 2.1.0** (build v0.3.8): `Cargo.lock` shows h2 = 0.4.5 -- VULNERABLE
- **RHTPA 2.1.1** (build v0.3.12): `Cargo.lock` shows h2 = 0.4.5 -- VULNERABLE (was missing from PSIRT assignment)
- **RHTPA 2.2.0** (build v0.4.5): `Cargo.lock` shows h2 = 0.4.8 -- NOT VULNERABLE (incorrectly included by PSIRT)

All 2.2.x versions (2.2.0 through 2.2.4) ship h2 >= 0.4.8 and are not affected.

## Jira Update

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
Based on lock file analysis at pinned commits from security-matrix.md.

- Removed RHTPA 2.2.0: ships h2 0.4.8 (at fix threshold, not vulnerable)
- Added RHTPA 2.1.1: ships h2 0.4.5 (below fix threshold, vulnerable)

This is an unscoped issue -- correction covers all streams.
Only 2.1.x stream versions are affected; all 2.2.x versions ship the patched h2.
```
