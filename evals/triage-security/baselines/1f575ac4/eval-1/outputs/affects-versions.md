# Step 3 -- Affects Versions Correction

## Current vs Proposed Affects Versions

The issue TC-8001 is **scoped to stream 2.2.x** (summary suffix `[rhtpa-2.2]`).

### PSIRT-assigned Affects Versions (current)

- RHTPA 2.0.0

### Problem

The current Affects Versions value `RHTPA 2.0.0` is **incorrect**:
1. There is no 2.0.x version stream in the Version Streams configuration.
2. The issue is scoped to the 2.2.x stream based on the `[rhtpa-2.2]` suffix.
3. Lock file analysis shows the affected 2.2.x versions are 2.2.0, 2.2.1, and 2.2.2.
4. Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fix version) and are NOT affected.

### Proposed Correction

| Change | Details |
|--------|---------|
| Remove | RHTPA 2.0.0 (does not exist as a valid version; no 2.0.x stream configured) |
| Add | RHTPA 2.2.0 (ships quinn-proto 0.11.9, affected) |
| Add | RHTPA 2.2.1 (ships quinn-proto 0.11.12, affected) |
| Add | RHTPA 2.2.2 (retag of 2.2.1, ships quinn-proto 0.11.12, affected) |

**Current:** `[RHTPA 2.0.0]`
**Proposed:** `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

### Rationale

Based on lock file analysis at pinned commits from security-matrix.md. The Cargo.lock at each build tag was inspected for the quinn-proto dependency version:
- v0.4.5 (2.2.0): quinn-proto 0.11.9 -- AFFECTED (< 0.11.14)
- v0.4.8 (2.2.1): quinn-proto 0.11.12 -- AFFECTED (< 0.11.14)
- v0.4.9 (2.2.2): retag of v0.4.8, same as 2.2.1 -- AFFECTED
- v0.4.11 (2.2.3): quinn-proto 0.11.14 -- NOT AFFECTED (>= 0.11.14)
- v0.4.12 (2.2.4): quinn-proto 0.11.14 -- NOT AFFECTED (>= 0.11.14)

Scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`. The 2.1.x stream versions (2.1.0, 2.1.1) are also affected but belong to a separate stream and would be tracked by a companion CVE Jira or via cross-stream proactive remediation (Step 7 Case B).

### Jira Update

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"name": "RHTPA 2.2.0"},
    {"name": "RHTPA 2.2.1"},
    {"name": "RHTPA 2.2.2"}
  ]
})
```

### Comment to Post

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

RHTPA 2.0.0 does not correspond to any configured version stream.
Versions 2.2.3 and 2.2.4 are not affected (ship quinn-proto 0.11.14, the fixed version).
```
