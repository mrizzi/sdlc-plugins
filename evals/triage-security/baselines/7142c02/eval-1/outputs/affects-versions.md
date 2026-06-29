# Step 3 -- Affects Versions Correction: TC-8001

## Current Affects Versions (PSIRT-assigned)

- RHTPA 2.0.0

## Problem

The PSIRT-assigned Affects Version `RHTPA 2.0.0` is incorrect. There is no `2.0.x` version stream configured in the Security Configuration. The configured streams are:

- **2.1.x** (Konflux release repo: `rhtpa-release.0.3.z`)
- **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`)

## Lock File Evidence

Based on version impact analysis from Step 2:

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.1.0 | 0.11.9 | YES |
| 2.1.1 | 0.11.9 | YES |
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | -- (retag of 2.2.1) | YES |
| 2.2.3 | 0.11.14 | NO |
| 2.2.4 | 0.11.14 | NO |

## Stream Scope

This issue is scoped to the **2.2.x** stream (from summary suffix `[rhtpa-2.2]`). The Affects Versions field should reflect only the versions within this stream that are actually affected.

## Proposed Correction

**Remove:** RHTPA 2.0.0 (does not exist as a configured stream)

**Add:** RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

These are the 2.2.x stream versions where quinn-proto is below 0.11.14 (the fix threshold). Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14, which is the fixed version, so they are not affected.

Note: Versions 2.1.0 and 2.1.1 (stream 2.1.x) are also affected but are outside this issue's stream scope. Cross-stream impact is handled via Step 7 Case B (preemptive remediation or cross-stream comment).

## Proposed Jira Mutation

```
jira.edit_issue("TC-8001", fields: {
  "versions": [
    { "name": "RHTPA 2.2.0" },
    { "name": "RHTPA 2.2.1" },
    { "name": "RHTPA 2.2.2" }
  ]
})
```

Rationale: PSIRT assigned `RHTPA 2.0.0` which does not correspond to any configured version stream. Lock file analysis confirms quinn-proto < 0.11.14 is present in versions 2.2.0, 2.2.1, and 2.2.2 within the issue's scoped stream (2.2.x). Versions 2.2.3 and 2.2.4 already ship the fixed version.
