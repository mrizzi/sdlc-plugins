# Step 3 -- Affects Versions Correction

## Current vs Proposed

| | Value |
|---|---|
| Current (PSIRT-assigned) | RHTPA 2.0.0 |
| Proposed (lock file evidence) | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Correction Rationale

The PSIRT-assigned Affects Version **RHTPA 2.0.0** is incorrect:

1. **RHTPA 2.0.0 does not exist** in the configured Version Streams. The supported streams are 2.1.x and 2.2.x. There is no 2.0.x stream configured.
2. This issue is **scoped to the 2.2.x stream** per the summary suffix `[rhtpa-2.2]`.
3. Lock file analysis at pinned commits from security-matrix.md shows:
   - **RHTPA 2.2.0** ships openssl-libs 3.0.7-25.el9_3 (AFFECTED -- before fix 3.0.7-28.el9_4)
   - **RHTPA 2.2.1** ships openssl-libs 3.0.7-27.el9_4 (AFFECTED -- before fix 3.0.7-28.el9_4)
   - **RHTPA 2.2.2** ships openssl-libs 3.0.7-27.el9_4 (AFFECTED -- retag of 2.2.1, same as 2.2.1)
   - RHTPA 2.2.3 ships openssl-libs 3.0.7-28.el9_4 (NOT affected -- equals fix version)
   - RHTPA 2.2.4 ships openssl-libs 3.0.7-28.el9_4 (NOT affected -- equals fix version)
4. Only versions within the 2.2.x stream scope are included. The 2.1.x stream versions (also affected) belong to a companion CVE issue for that stream.

## Proposed Jira Update

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
```

The Jira `versions` field would be updated using dynamically discovered version IDs from `getJiraIssueTypeMetaWithFields`, filtered by the RHTPA prefix.
