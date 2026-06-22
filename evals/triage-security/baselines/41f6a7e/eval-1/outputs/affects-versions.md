# Step 3 -- Affects Versions Correction

## Current vs Proposed

- **Current Affects Versions**: RHTPA 2.0.0
- **Issue stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)

### Stream-Scoped Analysis

Since this issue is scoped to stream 2.2.x (suffix `[rhtpa-2.2]`), only versions from the 2.2.x stream are included in the correction. The 2.1.x versions (2.1.0, 2.1.1) are also affected but belong to a companion issue for that stream.

Affected 2.2.x versions from the version impact table:
- RHTPA 2.2.0 -- quinn-proto 0.11.9 (affected)
- RHTPA 2.2.1 -- quinn-proto 0.11.12 (affected)
- RHTPA 2.2.2 -- retag of 2.2.1, quinn-proto 0.11.12 (affected)

Not affected 2.2.x versions:
- RHTPA 2.2.3 -- quinn-proto 0.11.14 (fixed)
- RHTPA 2.2.4 -- quinn-proto 0.11.14 (fixed)

### Correction

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

**Rationale**: PSIRT assigned "RHTPA 2.0.0" which does not exist as a supported version in the Version Streams configuration. Lock file analysis at pinned commits from security-matrix.md confirms that versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto versions within the vulnerable range (< 0.11.14). Versions 2.2.3 and 2.2.4 ship the fixed version 0.11.14 and are not affected. Correction is scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`.

### Cross-Stream Impact Notice

The version impact analysis also reveals that stream 2.1.x is affected:
- RHTPA 2.1.0 -- quinn-proto 0.11.9 (affected)
- RHTPA 2.1.1 -- quinn-proto 0.11.9 (affected)

These versions are outside this issue's stream scope and would be tracked by a companion Vulnerability issue for stream 2.1.x.

### Jira Operation (would execute after confirmation)

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-id>"},
    {"id": "<RHTPA-2.2.1-jira-id>"},
    {"id": "<RHTPA-2.2.2-jira-id>"}
  ]
})
```

Comment to add:
```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

RHTPA 2.0.0 does not exist as a supported version. Lock file evidence:
- 2.2.0 (v0.4.5): quinn-proto 0.11.9 (vulnerable)
- 2.2.1 (v0.4.8): quinn-proto 0.11.12 (vulnerable)
- 2.2.2 (v0.4.9): retag of 2.2.1 (vulnerable)
- 2.2.3 (v0.4.11): quinn-proto 0.11.14 (fixed)
- 2.2.4 (v0.4.12): quinn-proto 0.11.14 (fixed)
```
