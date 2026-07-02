# Step 3 -- Affects Versions Correction

## PROPOSAL: Correct Affects Versions on TC-8005

### Current State

PSIRT assigned **Affects Versions**: `RHTPA 2.0.0`

This is incorrect. There is no `2.0.x` version stream configured in the project's Security Configuration. The configured streams are 2.1.x and 2.2.x. Since the issue is scoped to the 2.2.x stream (per the `[rhtpa-2.2]` summary suffix), the Affects Versions should reflect only versions within that stream that actually ship the vulnerable openssl-libs.

### Lock File Evidence (rpms.lock.yaml)

| Version | openssl-libs | Affected? |
|---------|-------------|-----------|
| RHTPA 2.2.0 | 3.0.7-25.el9_3 | YES |
| RHTPA 2.2.1 | 3.0.7-27.el9_4 | YES |
| RHTPA 2.2.2 | (retag of 2.2.1) | YES |
| RHTPA 2.2.3 | 3.0.7-28.el9_4 | NO |
| RHTPA 2.2.4 | 3.0.7-28.el9_4 | NO |

### Proposed Correction

**Remove**: `RHTPA 2.0.0` (does not correspond to any configured version stream)

**Add**: `RHTPA 2.2.0`, `RHTPA 2.2.1`, `RHTPA 2.2.2`

**Do not add**: `RHTPA 2.2.3`, `RHTPA 2.2.4` (these versions already ship the fixed openssl-libs 3.0.7-28.el9_4)

### Rationale

The PSIRT-assigned Affects Version `RHTPA 2.0.0` does not match any configured version stream and is not supported by lock file evidence. The rpms.lock.yaml analysis confirms that openssl-libs versions before 3.0.7-28.el9_4 are present in versions 2.2.0 through 2.2.2. The fix was picked up in build 0.4.11 (version 2.2.3), so 2.2.3 and later are not affected.

Note: Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` at runtime. The version names above use the Jira version prefix `RHTPA` from Security Configuration.
