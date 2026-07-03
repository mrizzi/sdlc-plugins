# Step 3 -- Affects Versions Correction

## Current vs Proposed

| | Affects Versions |
|---|---|
| Current (PSIRT-assigned) | RHTPA 2.0.0 |
| Proposed (from lock file analysis) | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

The PSIRT-assigned Affects Version **RHTPA 2.0.0** is incorrect. There is no
2.0.x version stream in the product's Security Configuration -- the configured
streams are 2.1.x and 2.2.x. PSIRT likely assigned 2.0.0 based on scan time
rather than actual dependency analysis.

The issue is scoped to the **2.2.x** stream (per the `[rhtpa-2.2]` summary
suffix). Based on rpms.lock.yaml inspection at each pinned tag in the 2.2.x
supportability matrix:

- **RHTPA 2.2.0** (tag v0.4.5): openssl-libs 3.0.7-25.el9_3 -- AFFECTED (before fix 3.0.7-28.el9_4)
- **RHTPA 2.2.1** (tag v0.4.8): openssl-libs 3.0.7-27.el9_4 -- AFFECTED (before fix 3.0.7-28.el9_4)
- **RHTPA 2.2.2** (tag v0.4.9): retag of 2.2.1 -- AFFECTED (same as v0.4.8)
- **RHTPA 2.2.3** (tag v0.4.11): openssl-libs 3.0.7-28.el9_4 -- NOT AFFECTED (ships fixed version)
- **RHTPA 2.2.4** (tag v0.4.12): openssl-libs 3.0.7-28.el9_4 -- NOT AFFECTED (ships fixed version)

Versions 2.2.3 and 2.2.4 are excluded because they ship the fixed version.
Versions from the 2.1.x stream are excluded because this issue is scoped to
2.2.x -- the 2.1.x stream is tracked by a separate companion issue (if it exists).

## Proposed Jira Update

```
jira.edit_issue("TC-8005", fields={
  "versions": [
    {"name": "RHTPA 2.2.0"},
    {"name": "RHTPA 2.2.1"},
    {"name": "RHTPA 2.2.2"}
  ]
})
```

(Jira version IDs would be discovered dynamically via getJiraIssueTypeMetaWithFields
in a live triage.)

## Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
RHTPA 2.0.0 does not correspond to any configured version stream.
Versions 2.2.3+ ship the fixed openssl-libs 3.0.7-28.el9_4 and are not affected.
```
