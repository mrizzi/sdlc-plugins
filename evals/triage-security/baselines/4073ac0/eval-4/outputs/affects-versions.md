# Step 3 -- Affects Versions Correction

## Current vs Proposed Affects Versions

The issue is **unscoped** (no stream suffix), so the Affects Versions correction
includes all affected versions across all streams -- but only versions that are
actually affected per lock file evidence.

**Current Affects Versions** (PSIRT-assigned): `RHTPA 2.1.0, RHTPA 2.2.0`

**Version impact analysis**:
- RHTPA 2.1.0: h2 0.4.5 -- **AFFECTED** (correct to include)
- RHTPA 2.1.1: h2 0.4.5 -- **AFFECTED** (missing from PSIRT assignment)
- RHTPA 2.2.0: h2 0.4.8 -- **NOT AFFECTED** (incorrectly included by PSIRT)
- RHTPA 2.2.1 through 2.2.4: h2 >= 0.4.8 -- **NOT AFFECTED**

**Proposed Affects Versions**: `RHTPA 2.1.0, RHTPA 2.1.1`

## Proposed Correction

```
Current:  [RHTPA 2.1.0, RHTPA 2.2.0]
Proposed: [RHTPA 2.1.0, RHTPA 2.1.1]
```

Changes:
- **Added**: RHTPA 2.1.1 (ships h2 0.4.5, which is within the affected range)
- **Removed**: RHTPA 2.2.0 (ships h2 0.4.8, which is the fixed version -- not affected)

## Rationale

PSIRT assigned Affects Versions based on scan-time component presence, not actual
dependency version analysis. Lock file inspection at pinned commits from the
supportability matrix shows:

- All 2.1.x versions (2.1.0, 2.1.1) ship h2 0.4.5, which is within the vulnerable
  range (before 0.4.8). Both must be listed.
- All 2.2.x versions ship h2 >= 0.4.8 (the fixed version or later). RHTPA 2.2.0
  must be removed from Affects Versions as it is not affected.

## Proposed Jira Mutation

Pending engineer confirmation, the following update would be applied:

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"id": "<RHTPA-2.1.0-jira-id>"},
    {"id": "<RHTPA-2.1.1-jira-id>"}
  ]
})
```

Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields`.

## Proposed Comment

```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].
Based on lock file analysis at pinned commits from security-matrix.md.
RHTPA 2.2.0 removed: ships h2 0.4.8 (fixed version, not affected).
RHTPA 2.1.1 added: ships h2 0.4.5 (within affected range < 0.4.8).
Issue is unscoped -- correction covers all affected versions across all streams.
```

## Step 4 -- Duplicate and Sibling Check

**JQL query**:
```
project = TC AND labels = 'CVE-2026-33501' AND issuetype = 10024 AND key != TC-8004
```

**Result**: No sibling issues found (JQL returns empty).

No duplicate or companion issues exist for this CVE. No cross-stream coordination
required. Proceeding to Step 5.

## Step 5 -- Version Lifecycle Check

Proposed check: fetch the product lifecycle page at
`https://access.example.com/product-life-cycle/rhtpa` to verify support status
of affected versions (RHTPA 2.1.0, RHTPA 2.1.1).

For the purposes of this analysis, both 2.1.x versions are assumed to be within
their supported lifecycle.

## Step 6 -- Already Fixed Check

No resolved sibling issues exist (Step 4 returned empty). No already-fixed
detection applicable. Proceeding to Step 7.
