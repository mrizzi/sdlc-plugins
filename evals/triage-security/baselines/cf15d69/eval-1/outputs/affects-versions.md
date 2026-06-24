# Step 3 -- Affects Versions Correction: TC-8001

## Current vs Proposed Affects Versions

| | Value |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.0.0 |
| **Proposed (lock file evidence)** | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

The PSIRT-assigned Affects Version "RHTPA 2.0.0" is incorrect:
- There is no 2.0.x version stream configured in the project's Security Configuration.
- No "RHTPA 2.0.0" version exists in the Jira version registry.
- The issue summary suffix `[rhtpa-2.2]` indicates this issue is scoped to the **2.2.x** stream.

Based on lock file analysis at pinned commits from security-matrix.md:
- **RHTPA 2.2.0** (tag v0.4.5): quinn-proto 0.11.9 -- AFFECTED (< 0.11.14)
- **RHTPA 2.2.1** (tag v0.4.8): quinn-proto 0.11.12 -- AFFECTED (< 0.11.14)
- **RHTPA 2.2.2** (tag v0.4.9): retag of 2.2.1 -- AFFECTED (same as 2.2.1)
- **RHTPA 2.2.3** (tag v0.4.11): quinn-proto 0.11.14 -- NOT AFFECTED (>= 0.11.14)
- **RHTPA 2.2.4** (tag v0.4.12): quinn-proto 0.11.14 -- NOT AFFECTED (>= 0.11.14)

Since this issue is scoped to the 2.2.x stream, only 2.2.x versions are included.
The 2.1.x stream versions (2.1.0, 2.1.1) are also affected but belong to a separate
stream and would be tracked by a companion CVE issue or preemptive remediation tasks.

## Proposed Jira Mutation

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-id>"},
    {"id": "<RHTPA-2.2.1-jira-id>"},
    {"id": "<RHTPA-2.2.2-jira-id>"}
  ]
})
```

## Comment to Post

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

RHTPA 2.0.0 does not correspond to any configured version stream and is not a valid
Jira version. The correct affected versions in the 2.2.x stream are 2.2.0 through 2.2.2,
which ship quinn-proto 0.11.9-0.11.12 (vulnerable range: < 0.11.14).

Versions 2.2.3+ ship quinn-proto 0.11.14 (the fixed version) and are not affected.
```
