# Step 3 -- Affects Versions Correction

## Current Affects Versions (PSIRT-assigned)

- **RHTPA 2.0.0**

## Issue Stream Scope

This issue is scoped to the **2.2.x** stream (summary suffix: `[rhtpa-2.2]`).

Per the triage-security methodology, Affects Versions correction is scoped to the issue's stream. Since this issue is scoped to 2.2.x, we only set Affects Versions for versions within the 2.2.x stream that are actually affected.

## Version Impact Evidence (2.2.x stream only)

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.11.14 | NO | fixed version |
| 2.2.4 | 0.11.14 | NO | fixed version |

## Proposed Correction

**Remove**: RHTPA 2.0.0 (incorrect -- no 2.0.x stream exists in the configured Version Streams; this version does not correspond to any supported product version)

**Add**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

**Rationale**: The PSIRT-assigned Affects Version "RHTPA 2.0.0" is incorrect. There is no 2.0.x version stream configured in the Security Configuration. Lock file analysis shows that within the issue-scoped 2.2.x stream, versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto versions below 0.11.14 (the fix threshold). Versions 2.2.3 and 2.2.4 already ship the fixed version (0.11.14) and are NOT affected.

Note: Version 2.2.2 is a retag of 2.2.1 (build tag v0.4.9 is a retag of v0.4.8). The affected status is carried forward from 2.2.1.

## Cross-Stream Impact Notice

The 2.1.x stream is also affected (versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9), but this issue is scoped to 2.2.x only. Cross-stream impact would be noted via a comment on TC-8001 per Case B of Step 7 (see remediation output).

## Proposed Jira Mutation

```
jira.edit_issue(
  id: "TC-8001",
  fields: {
    "versions": [
      {"name": "RHTPA 2.2.0"},
      {"name": "RHTPA 2.2.1"},
      {"name": "RHTPA 2.2.2"}
    ]
  }
)
```

This mutation requires engineer confirmation before execution.
