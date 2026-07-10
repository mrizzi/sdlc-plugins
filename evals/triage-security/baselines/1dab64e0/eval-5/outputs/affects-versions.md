# Step 3 -- Affects Versions Correction

## Current vs Proposed

| | Value |
|---|---|
| Current Affects Versions (PSIRT-assigned) | RHTPA 2.0.0 |
| Proposed Affects Versions | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

The PSIRT-assigned Affects Version "RHTPA 2.0.0" is incorrect. There is no
2.0.x stream configured in the Version Streams table, and lock file analysis
shows the actual affected versions within the scoped 2.2.x stream are:

- **RHTPA 2.2.0** -- openssl-libs 3.0.7-25.el9_3 (vulnerable, before fix 3.0.7-28.el9_4)
- **RHTPA 2.2.1** -- openssl-libs 3.0.7-27.el9_4 (vulnerable, before fix 3.0.7-28.el9_4)
- **RHTPA 2.2.2** -- openssl-libs 3.0.7-27.el9_4 (retag of 2.2.1, same vulnerable version)

Versions 2.2.3 and 2.2.4 ship the fixed openssl-libs 3.0.7-28.el9_4 and are
excluded from Affects Versions.

The correction is scoped to the 2.2.x stream per the issue suffix `[rhtpa-2.2]`.
The 2.1.x stream versions (also affected) belong to a companion CVE issue for
that stream, if one exists, or will be addressed via preemptive remediation
tasks (Step 8 Case B).

## Jira Mutation (would execute after engineer confirmation)

```
jira.edit_issue("TC-8005", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-id>"},
    {"id": "<RHTPA-2.2.1-jira-id>"},
    {"id": "<RHTPA-2.2.2-jira-id>"}
  ]
})
```

Jira version IDs would be discovered dynamically via
`getJiraIssueTypeMetaWithFields` (Step 3.1) -- not hardcoded.

## Comment (would post after engineer confirmation)

```
Corrected Affects Versions: [RHTPA 2.0.0] --> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

RHTPA 2.0.0 does not correspond to a configured version stream.
Versions 2.2.3 and 2.2.4 ship the fixed openssl-libs 3.0.7-28.el9_4 and are not affected.
```
