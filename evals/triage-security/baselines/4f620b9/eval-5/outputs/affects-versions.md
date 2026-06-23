# Step 3 - Affects Versions Correction

## Current State

- **Current Affects Versions**: RHTPA 2.0.0
- **Issue stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)

## Analysis

The PSIRT-assigned Affects Versions value "RHTPA 2.0.0" is incorrect for this issue. There is no 2.0.x stream configured in the Version Streams table, so "RHTPA 2.0.0" does not correspond to any supported version stream.

Based on the version impact analysis using rpms.lock.yaml data, the affected versions within the 2.2.x stream are:

- **RHTPA 2.2.0** — ships openssl-libs 3.0.7-25.el9_3 (vulnerable)
- **RHTPA 2.2.1** — ships openssl-libs 3.0.7-27.el9_4 (vulnerable)
- **RHTPA 2.2.2** — retag of 2.2.1, same openssl-libs 3.0.7-27.el9_4 (vulnerable)

Versions 2.2.3 and 2.2.4 ship openssl-libs 3.0.7-28.el9_4 (the fixed version) and are NOT affected.

## Proposed Correction

**Remove**: RHTPA 2.0.0
**Add**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

This correction would be performed via Jira API after engineer confirmation:

```
jira.edit_issue(TC-8005, {
  "versions": [
    {"name": "RHTPA 2.2.0"},
    {"name": "RHTPA 2.2.1"},
    {"name": "RHTPA 2.2.2"}
  ]
})
```

**Rationale**: Lock file evidence from rpms.lock.yaml at each pinned tag shows that versions 2.2.0 through 2.2.2 ship openssl-libs at versions prior to the fix (3.0.7-28.el9_4). Versions 2.2.3 and 2.2.4 already include the patched openssl-libs and are not affected. The original PSIRT-assigned value of RHTPA 2.0.0 does not correspond to any configured version stream and was likely assigned based on scan time rather than dependency analysis.

**Note**: This is a proposed correction. The actual Jira update would only be executed after explicit engineer confirmation.
