# Step 3 -- Affects Versions Correction: TC-8004

## Current vs Proposed Affects Versions

The issue is **unscoped** (no stream suffix), so Affects Versions should include all affected versions across all streams -- but only versions that are actually affected per the lock file evidence.

| | Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.1.0, RHTPA 2.2.0 |
| **Proposed (lock file evidence)** | RHTPA 2.1.0, RHTPA 2.1.1 |

## Correction Details

### Versions to ADD

| Version | Reason |
|---------|--------|
| RHTPA 2.1.1 | Ships h2 0.4.5 (vulnerable, < 0.4.8) -- missing from PSIRT assignment |

### Versions to REMOVE

| Version | Reason |
|---------|--------|
| RHTPA 2.2.0 | Ships h2 0.4.8 (fixed version) -- NOT affected |

### Versions RETAINED (correct)

| Version | Reason |
|---------|--------|
| RHTPA 2.1.0 | Ships h2 0.4.5 (vulnerable, < 0.4.8) -- correctly assigned by PSIRT |

## Rationale

PSIRT assigned Affects Versions based on scan time, including RHTPA 2.2.0. However, lock file analysis at pinned source commits shows:

- **RHTPA 2.1.0** (tag `v0.3.8`): h2 = 0.4.5 --> AFFECTED (below fix threshold 0.4.8)
- **RHTPA 2.1.1** (tag `v0.3.12`): h2 = 0.4.5 --> AFFECTED (below fix threshold 0.4.8) -- was missing
- **RHTPA 2.2.0** (tag `v0.4.5`): h2 = 0.4.8 --> NOT AFFECTED (meets fix threshold)

The correction scopes Affects Versions to only the versions that actually ship the vulnerable h2 dependency. All 2.2.x versions ship h2 >= 0.4.8 and are not affected.

## Proposed Jira Update

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"name": "RHTPA 2.1.0"},
    {"name": "RHTPA 2.1.1"}
  ]
})
```

Comment to post on TC-8004:
```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
Based on lock file analysis at pinned commits from security-matrix.md.

Evidence:
- RHTPA 2.1.0 (v0.3.8): h2 = 0.4.5 (vulnerable, < 0.4.8)
- RHTPA 2.1.1 (v0.3.12): h2 = 0.4.5 (vulnerable, < 0.4.8)
- RHTPA 2.2.0 (v0.4.5): h2 = 0.4.8 (fixed version, NOT affected) -- removed

Issue is unscoped -- correction includes all affected versions across all streams.
Only 2.1.x stream versions are affected; all 2.2.x versions ship patched h2.
```
