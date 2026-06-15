# Version Impact

## Library: h2 | Fixed version: 0.4.8 | Affected: < 0.4.8

Since the issue is **unscoped**, all streams are checked.

| Version | Stream | Build Tag | h2 | Affected? | Notes |
|---------|--------|-----------|-----|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | YES | < 0.4.8 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | YES | < 0.4.8 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | >= 0.4.8 |
| 2.2.2 | 2.2.x | v0.4.9 | 0.4.8 | NO | retag of 2.2.1 |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | >= 0.4.8 |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | >= 0.4.8 |

## Summary

Mixed results across streams:

- **2.1.x stream**: AFFECTED -- all versions (2.1.0, 2.1.1) ship h2 0.4.5 which is below the fixed version 0.4.8
- **2.2.x stream**: NOT affected -- all versions ship h2 >= 0.4.8 (the fix)
