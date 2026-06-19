# Step 3 — Affects Versions Correction

## Current vs Proposed

The issue TC-8005 is scoped to stream **2.2.x** (suffix `[rhtpa-2.2]`).
Only versions within the 2.2.x stream are included in the correction.

| | Affects Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.0.0 |
| **Proposed (lock file evidence)** | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

- **RHTPA 2.0.0** is incorrect — no `2.0.x` stream exists in the configured Version
  Streams. PSIRT likely assigned this as a placeholder or based on scan-time defaults.
- **RHTPA 2.2.0** — ships openssl-libs 3.0.7-25.el9_3, which is within the affected
  range (< 3.0.7-28.el9_4). Affected.
- **RHTPA 2.2.1** — ships openssl-libs 3.0.7-27.el9_4, which is within the affected
  range (< 3.0.7-28.el9_4). Affected.
- **RHTPA 2.2.2** — retag of 2.2.1 (same openssl-libs 3.0.7-27.el9_4). Affected.
- **RHTPA 2.2.3** — ships openssl-libs 3.0.7-28.el9_4, the fixed version. Not affected.
- **RHTPA 2.2.4** — ships openssl-libs 3.0.7-28.el9_4, the fixed version. Not affected.

## Correction Details

Remove RHTPA 2.0.0 (invalid version). Add RHTPA 2.2.0, RHTPA 2.2.1, and RHTPA 2.2.2
as the affected versions within the 2.2.x stream scope.

The 2.1.x stream versions (RHTPA 2.1.0, RHTPA 2.1.1) are also affected but belong to
a companion Vulnerability issue scoped to that stream — they are not included in this
issue's Affects Versions.

## Jira Mutation (would execute after engineer confirmation)

```
jira.edit_issue("TC-8005", fields={
  "versions": [
    {"id": "<jira-id-for-RHTPA-2.2.0>"},
    {"id": "<jira-id-for-RHTPA-2.2.1>"},
    {"id": "<jira-id-for-RHTPA-2.2.2>"}
  ]
})
```

Comment to post:
```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
```
