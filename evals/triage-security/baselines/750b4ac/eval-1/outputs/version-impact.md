# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

All versions from both streams (2.1.x and 2.2.x) are included for full coverage, even though this issue is scoped to 2.2.x only.

### Version Impact Table

| Version | Stream | Pinned Tag | quinn-proto | Affected? | Notes |
|---------|--------|------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | < 0.11.14 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 2.2.x | `v0.4.8` | -- | YES | retag of 2.2.1 (same backend tag v0.4.8); result carried forward |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Method

For each released version, the quinn-proto dependency version was extracted from `Cargo.lock` at the pinned backend commit tag listed in the supportability matrix:

```
git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'
```

Version 2.2.2 is a retag of 2.2.1 -- both use backend tag `v0.4.8`. The lock file check was skipped for 2.2.2 and the result (quinn-proto 0.11.12, AFFECTED) was carried forward from 2.2.1.

### Affected Range Logic

- Affected range: versions before 0.11.14 (< 0.11.14)
- Fixed version: 0.11.14
- quinn-proto 0.11.9 --> AFFECTED (0.11.9 < 0.11.14)
- quinn-proto 0.11.12 --> AFFECTED (0.11.12 < 0.11.14)
- quinn-proto 0.11.14 --> NOT AFFECTED (0.11.14 >= 0.11.14)

### Stream-Scoped Summary

This issue is scoped to **2.2.x** (per suffix `[rhtpa-2.2]`):

- **Affected 2.2.x versions**: 2.2.0, 2.2.1, 2.2.2
- **Not affected 2.2.x versions**: 2.2.3, 2.2.4
- **2.1.x versions** (out of scope for this issue): 2.1.0 and 2.1.1 are also affected but belong to a separate stream

### Cross-Stream Observation

The 2.1.x stream (versions 2.1.0, 2.1.1) also ships a vulnerable quinn-proto (0.11.9). This is outside the scope of TC-8001 but will be noted as cross-stream impact in Step 7.
