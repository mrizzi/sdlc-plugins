# Affects Versions Correction — TC-8004

## PROPOSAL: Correct Affects Versions on TC-8004

### Current Affects Versions (PSIRT-assigned)

- RHTPA 2.1.0
- RHTPA 2.2.0

### Proposed Affects Versions (based on lock file evidence)

- RHTPA 2.1.0
- RHTPA 2.1.1

### Changes

| Action | Version | Reason |
|--------|---------|--------|
| Keep | RHTPA 2.1.0 | Affected: ships h2 0.4.5 (< 0.4.8) |
| Add | RHTPA 2.1.1 | Affected: ships h2 0.4.5 (< 0.4.8) — missing from PSIRT assignment |
| Remove | RHTPA 2.2.0 | Not affected: ships h2 0.4.8 (the fixed version) |

### Rationale

PSIRT assigned Affects Versions based on scan time, not actual dependency analysis. Lock file inspection at pinned source commits shows:

- **RHTPA 2.1.0** (tag v0.3.8): `Cargo.lock` contains h2 0.4.5 — AFFECTED (< 0.4.8)
- **RHTPA 2.1.1** (tag v0.3.12): `Cargo.lock` contains h2 0.4.5 — AFFECTED (< 0.4.8), but was not listed by PSIRT
- **RHTPA 2.2.0** (tag v0.4.5): `Cargo.lock` contains h2 0.4.8 — NOT AFFECTED (>= 0.4.8, the fix version)

All other 2.2.x versions (2.2.1 through 2.2.4) also ship h2 >= 0.4.8 and are not affected. Only the 2.1.x stream versions are affected.

### Jira Mutation (proposed)

```
jira.edit_issue("TC-8004", {
  "versions": [
    {"name": "RHTPA 2.1.0"},
    {"name": "RHTPA 2.1.1"}
  ]
})
```

This mutation requires engineer confirmation before execution.
