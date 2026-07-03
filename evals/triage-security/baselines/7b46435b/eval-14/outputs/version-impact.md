# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

Stream scope: **2.2.x** (per issue suffix `[rhtpa-2.2]`)

| Version | Tag | openssl-libs version | Affected? | Notes |
|---------|-----|----------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | before fixed version 3.0.7-28.el9_4 |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | before fixed version 3.0.7-28.el9_4 |
| 2.2.2 | v0.4.9 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | equals fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | equals fixed version |

## Summary

- **Affected versions**: 2.2.0, 2.2.1, 2.2.2
- **Not affected versions**: 2.2.3, 2.2.4
- Versions 2.2.3 and 2.2.4 ship openssl-libs 3.0.7-28.el9_4 which is the fixed version.
- Version 2.2.2 is a retag of 2.2.1 (backend tag v0.4.9 is identical to v0.4.8), so the openssl-libs version is carried forward from 2.2.1.

## Cross-Stream Impact

The 2.1.x stream (outside this issue's scope) also ships vulnerable openssl-libs versions:

| Version | Tag | openssl-libs version | Affected? |
|---------|-----|----------------------|-----------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES |

This cross-stream impact would be reported via Case B (proactive remediation) in Step 8, but is outside the scope of this stream-scoped issue.
