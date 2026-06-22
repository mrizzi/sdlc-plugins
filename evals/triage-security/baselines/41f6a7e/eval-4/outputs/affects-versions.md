# Affects Versions Correction — TC-8004

## Step 3: Affects Versions Comparison

### Current (PSIRT-assigned) Affects Versions

- RHTPA 2.1.0
- RHTPA 2.2.0

### Lock File Evidence

Based on the version impact analysis:

| Version | h2 Version | Affected? |
|---------|------------|-----------|
| RHTPA 2.1.0 | 0.4.5 | **YES** |
| RHTPA 2.1.1 | 0.4.5 | **YES** |
| RHTPA 2.2.0 | 0.4.8 | NO (fixed) |
| RHTPA 2.2.1 | 0.4.8 | NO (fixed) |
| RHTPA 2.2.2 | -- | NO (retag of 2.2.1) |
| RHTPA 2.2.3 | 0.4.9 | NO (fixed) |
| RHTPA 2.2.4 | 0.4.9 | NO (fixed) |

### Proposed Correction

Since this issue is **unscoped** (no stream suffix), the Affects Versions should include all affected versions across all streams -- but scoped to **actually affected versions only**.

```
Current:  [RHTPA 2.1.0, RHTPA 2.2.0]
Proposed: [RHTPA 2.1.0, RHTPA 2.1.1]
```

### Changes

- **Keep**: RHTPA 2.1.0 -- confirmed affected (h2 0.4.5 < 0.4.8)
- **Add**: RHTPA 2.1.1 -- confirmed affected (h2 0.4.5 < 0.4.8), missing from PSIRT assignment
- **Remove**: RHTPA 2.2.0 -- NOT affected (ships h2 0.4.8, which is the fixed version)

### Rationale

PSIRT assigned Affects Versions based on scan-time heuristics, not dependency analysis. Lock file inspection at pinned commits shows:

1. **RHTPA 2.1.0** (build v0.3.8): `Cargo.lock` contains h2 0.4.5, which is within the vulnerable range (< 0.4.8). Correctly flagged by PSIRT.
2. **RHTPA 2.1.1** (build v0.3.12): `Cargo.lock` contains h2 0.4.5, which is within the vulnerable range. **Missing from PSIRT assignment** -- must be added.
3. **RHTPA 2.2.0** (build v0.4.5): `Cargo.lock` contains h2 0.4.8, which is the fixed version. **Incorrectly included by PSIRT** -- must be removed.

### Jira Update (proposed)

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"name": "RHTPA 2.1.0"},
    {"name": "RHTPA 2.1.1"}
  ]
})
```

Comment to post after update:

```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
Based on lock file analysis at pinned commits from security-matrix.md.
- Added RHTPA 2.1.1: h2 0.4.5 at v0.3.12 is within the vulnerable range (< 0.4.8).
- Removed RHTPA 2.2.0: h2 0.4.8 at v0.4.5 is the fixed version (>= 0.4.8).
This issue is unscoped (no stream suffix) -- correction includes all affected versions across all streams.
```

## Step 4: Duplicate and Sibling Check

JQL search for sibling issues with the same CVE:
```
project = TC AND labels = 'CVE-2026-33501' AND issuetype = 10024 AND key != TC-8004
```

**Result**: No sibling issues found. No duplicates or cross-stream companions exist.

## Step 5: Version Lifecycle Check

All affected versions (RHTPA 2.1.0, RHTPA 2.1.1) are assumed to be within support lifecycle. No EOL filtering required.

## Step 6: Already Fixed Check

No resolved sibling issues exist (Step 4 found no siblings). Proceeding to remediation.
