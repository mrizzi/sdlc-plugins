# Step 3 -- Affects Versions Correction

## Current vs Proposed Affects Versions

Since TC-8004 is **unscoped** (no stream suffix), the Affects Versions field should include all actually affected versions across all streams -- but only those versions that are actually vulnerable based on lock file evidence.

| | Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.1.0, RHTPA 2.2.0 |
| **Proposed (lock file evidence)** | RHTPA 2.1.0, RHTPA 2.1.1 |

## Correction Details

- **Remove RHTPA 2.2.0**: Lock file analysis shows RHTPA 2.2.0 (build tag v0.4.5) ships h2 0.4.8, which is the fixed version. RHTPA 2.2.0 is NOT affected.
- **Add RHTPA 2.1.1**: Lock file analysis shows RHTPA 2.1.1 (build tag v0.3.12) ships h2 0.4.5, which is within the vulnerable range (< 0.4.8). PSIRT did not include this version.
- **Keep RHTPA 2.1.0**: Lock file analysis confirms RHTPA 2.1.0 (build tag v0.3.8) ships h2 0.4.5 -- correctly identified as affected by PSIRT.

## Proposed Jira Mutation

```
Proposed action: Update Affects Versions on TC-8004

Current:  [RHTPA 2.1.0, RHTPA 2.2.0]
Proposed: [RHTPA 2.1.0, RHTPA 2.1.1]

Rationale:
- RHTPA 2.2.0 removed: ships h2 0.4.8 (fixed version, not vulnerable)
- RHTPA 2.1.1 added: ships h2 0.4.5 (vulnerable, within affected range < 0.4.8)

jira.edit_issue("TC-8004", fields={
  "versions": [{"id": "<RHTPA-2.1.0-jira-id>"}, {"id": "<RHTPA-2.1.1-jira-id>"}]
})
```

## Proposed Comment

```
jira.add_comment("TC-8004", "Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].

Based on lock file analysis at pinned commits from security-matrix.md:
- RHTPA 2.1.0 (v0.3.8): h2 0.4.5 -- AFFECTED
- RHTPA 2.1.1 (v0.3.12): h2 0.4.5 -- AFFECTED
- RHTPA 2.2.0 (v0.4.5): h2 0.4.8 -- NOT AFFECTED (ships fixed version)
- All other 2.2.x versions: h2 >= 0.4.8 -- NOT AFFECTED

Issue is unscoped (no stream suffix); Affects Versions scoped to all actually affected versions across streams.")
```

_Awaiting engineer confirmation before executing._
