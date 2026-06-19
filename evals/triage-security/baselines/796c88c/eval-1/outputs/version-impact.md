# Step 2: Version Impact Analysis

## Vulnerability Criteria

- **Library**: quinn-proto
- **Affected range**: versions before 0.11.14
- **Fixed version**: 0.11.14

## Impact Table

| Version | Stream | Build Tag | quinn-proto Version | Affected | Notes |
|---------|--------|-----------|---------------------|----------|-------|
| RHTPA 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | Yes | 0.11.9 < 0.11.14 |
| RHTPA 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | Yes | 0.11.9 < 0.11.14 |
| RHTPA 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | Yes | 0.11.9 < 0.11.14 |
| RHTPA 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | Yes | 0.11.12 < 0.11.14 |
| RHTPA 2.2.2 | 2.2.x | `v0.4.8` | _(carry forward)_ | Yes | Retag of 2.2.1. Carries forward quinn-proto 0.11.12. |
| RHTPA 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | No | 0.11.14 is the fixed version |
| RHTPA 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | No | 0.11.14 is the fixed version |

## Summary

- **Affected versions**: RHTPA 2.1.0, RHTPA 2.1.1, RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Not affected versions**: RHTPA 2.2.3, RHTPA 2.2.4
- **First fixed version**: RHTPA 2.2.3 (ships quinn-proto 0.11.14)

### Retag Handling

RHTPA 2.2.2 is a retag of 2.2.1 for the backend component (supportability matrix note: "backend retag of 2.2.1"). The lock file check was skipped; the quinn-proto version is carried forward from RHTPA 2.2.1 (0.11.12, affected).
