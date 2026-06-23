# Step 3 -- Affects Versions Correction: TC-8001

## Current vs Proposed Affects Versions

The issue TC-8001 is **scoped to stream 2.2.x** (per summary suffix `[rhtpa-2.2]`). Only versions within the 2.2.x stream should be included in this issue's Affects Versions.

### PSIRT-assigned Affects Versions (current)

- RHTPA 2.0.0

### Version Impact (2.2.x stream only, per issue scope)

| Version | Affected? |
|---------|-----------|
| RHTPA 2.2.0 | YES (quinn-proto 0.11.9) |
| RHTPA 2.2.1 | YES (quinn-proto 0.11.12) |
| RHTPA 2.2.2 | YES (retag of 2.2.1) |
| RHTPA 2.2.3 | NO (quinn-proto 0.11.14 -- fixed) |
| RHTPA 2.2.4 | NO (quinn-proto 0.11.14 -- fixed) |

### Correction

**PSIRT version is wrong.** `RHTPA 2.0.0` does not correspond to any configured version stream (no 2.0.x stream exists in the Version Streams table).

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

### Rationale

- `RHTPA 2.0.0` is removed because no 2.0.x version stream exists in the security configuration. This appears to be a PSIRT data entry error.
- `RHTPA 2.2.0` is added because lock file analysis at build tag v0.4.5 shows quinn-proto 0.11.9, which is within the affected range (< 0.11.14).
- `RHTPA 2.2.1` is added because lock file analysis at build tag v0.4.8 shows quinn-proto 0.11.12, which is within the affected range (< 0.11.14).
- `RHTPA 2.2.2` is added because it is a retag of 2.2.1 (same build artifacts as v0.4.8), so the same vulnerable quinn-proto 0.11.12 is shipped.
- `RHTPA 2.2.3` and `RHTPA 2.2.4` are excluded because they ship quinn-proto 0.11.14, which is the fixed version.

### Cross-Stream Note

Versions 2.1.0 and 2.1.1 (stream 2.1.x) are also affected but belong to a different stream. They are NOT included in this issue's Affects Versions because TC-8001 is scoped to 2.2.x. The 2.1.x impact is handled via cross-stream remediation (see Step 7, Case B).

### Proposed Jira Mutation

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"name": "RHTPA 2.2.0"},
    {"name": "RHTPA 2.2.1"},
    {"name": "RHTPA 2.2.2"}
  ]
})
```

Note: Actual version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (Step 3.1). The names above are illustrative.

### Proposed Jira Comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

RHTPA 2.0.0 removed -- no 2.0.x version stream exists in the security configuration.
RHTPA 2.2.3 and 2.2.4 excluded -- ship quinn-proto 0.11.14 (fixed version).
```
