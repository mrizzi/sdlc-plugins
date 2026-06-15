# Step 2: Version Impact Analysis

## Vulnerability Criteria

- **Library**: h2
- **Affected range**: < 0.4.8
- **Fixed version**: 0.4.8
- **Ecosystem**: Cargo
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`

## Scope

UNSCOPED — analyzing ALL streams (2.1.x and 2.2.x).

## Version Impact Table

| Version | Stream | Tag | h2 version | Affected? | Notes |
|---------|--------|-----|------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.4.5 | YES | < 0.4.8 — vulnerable |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.4.5 | YES | < 0.4.8 — vulnerable |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.4.8 | NO | >= 0.4.8 — ships fixed version |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.4.8 | NO | >= 0.4.8 — ships fixed version |
| 2.2.2 | 2.2.x | `v0.4.9` | 0.4.8 | NO | retag of v0.4.8, carry forward from 2.2.1 |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.4.9 | NO | >= 0.4.8 — ships patched version |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.4.9 | NO | >= 0.4.8 — ships patched version |

## Stream Impact Summary

| Stream | Affected? | Details |
|--------|-----------|---------|
| 2.1.x | YES | All versions (2.1.0, 2.1.1) ship h2 0.4.5 which is vulnerable |
| 2.2.x | NO | All versions ship h2 >= 0.4.8 (the fixed version or later) |

**Result**: MIXED — the 2.1.x stream is affected, the 2.2.x stream is not affected. Remediation is required only for the 2.1.x stream.
