# Step 3 -- Affects Versions Correction

## Current vs Proposed

The PSIRT-assigned Affects Versions is incorrect. It references a version (RHTPA 2.0.0) that does not correspond to any version in the 2.2.x stream.

**Current**: RHTPA 2.0.0
**Proposed**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

## Rationale

Based on lock file analysis of `rpms.lock.yaml` at pinned commits from the supportability matrix:

- **RHTPA 2.2.0** (tag v0.4.5): openssl-libs 3.0.7-25.el9_3 -- affected (< 3.0.7-28.el9_4)
- **RHTPA 2.2.1** (tag v0.4.8): openssl-libs 3.0.7-27.el9_4 -- affected (< 3.0.7-28.el9_4)
- **RHTPA 2.2.2** (tag v0.4.9): retag of 2.2.1 -- affected (same as 2.2.1)
- **RHTPA 2.2.3** (tag v0.4.11): openssl-libs 3.0.7-28.el9_4 -- NOT affected (= fixed version)
- **RHTPA 2.2.4** (tag v0.4.12): openssl-libs 3.0.7-28.el9_4 -- NOT affected (= fixed version)

Scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`. Versions 2.1.0 and 2.1.1 are also affected but belong to the 2.1.x stream and are tracked by a companion issue.

## Jira Mutation

```
jira.edit_issue("TC-8005", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-id>"},
    {"id": "<RHTPA-2.2.1-jira-id>"},
    {"id": "<RHTPA-2.2.2-jira-id>"}
  ]
})
```

Version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields`.

## Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis (rpms.lock.yaml) at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
```
