# Step 3 -- Affects Versions Correction

## Current vs Proposed

The issue TC-8005 is scoped to stream **2.2.x** per the summary suffix `[rhtpa-2.2]`.
Only versions belonging to the 2.2.x stream are included in the correction.

| | Affects Versions |
|---|---|
| **Current (PSIRT-assigned)** | RHTPA 2.0.0 |
| **Proposed (lock file evidence)** | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

- **RHTPA 2.0.0 is incorrect**: There is no 2.0.x version stream configured in
  Security Configuration, and no version 2.0.0 exists in the supportability matrix.
  PSIRT likely assigned this as a placeholder or based on scan-time heuristics.

- **RHTPA 2.2.0** (build v0.4.5): ships openssl-libs 3.0.7-25.el9_3, which is
  before the fixed version 3.0.7-28.el9_4. **Affected.**

- **RHTPA 2.2.1** (build v0.4.8): ships openssl-libs 3.0.7-27.el9_4, which is
  before the fixed version 3.0.7-28.el9_4. **Affected.**

- **RHTPA 2.2.2** (build v0.4.9): retag of 2.2.1, same openssl-libs version
  (3.0.7-27.el9_4). **Affected.**

- **RHTPA 2.2.3** (build v0.4.11): ships openssl-libs 3.0.7-28.el9_4, which
  equals the fixed version. **Not affected.**

- **RHTPA 2.2.4** (build v0.4.12): ships openssl-libs 3.0.7-28.el9_4, which
  equals the fixed version. **Not affected.**

## Cross-stream note

Versions in the 2.1.x stream (RHTPA 2.1.0, RHTPA 2.1.1) are also affected but
are excluded from this correction because TC-8005 is scoped to the 2.2.x stream.
The 2.1.x versions are tracked by their own stream-specific CVE issue (if one
exists) or flagged for cross-stream impact in Step 8 Case B.

## Proposed Jira comment

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned build tags from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

Evidence:
- 2.2.0 (v0.4.5): openssl-libs 3.0.7-25.el9_3 (vulnerable)
- 2.2.1 (v0.4.8): openssl-libs 3.0.7-27.el9_4 (vulnerable)
- 2.2.2 (v0.4.9): retag of 2.2.1 (vulnerable)
- 2.2.3 (v0.4.11): openssl-libs 3.0.7-28.el9_4 (fixed)
- 2.2.4 (v0.4.12): openssl-libs 3.0.7-28.el9_4 (fixed)
```
