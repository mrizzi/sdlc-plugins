# Step 4-5: Version Impact Analysis

## Vulnerability Criteria

- **Library**: serde_json
- **Affected range**: < 1.0.135
- **Fixed version**: 1.0.135
- **Ecosystem**: Cargo
- **Lock file**: Cargo.lock
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'`

## Primary Scope: 2.2.x Stream

The issue summary contains [rhtpa-2.2], scoping the primary analysis to the 2.2.x stream.

| Version | Stream | Build Tag | serde_json | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.2.0 | 2.2.x | v0.4.5 | 1.0.138 | NO | >= 1.0.135 |
| 2.2.1 | 2.2.x | v0.4.8 | 1.0.138 | NO | >= 1.0.135 |
| 2.2.2 | 2.2.x | v0.4.9 | 1.0.138 | NO | retag of 2.2.1 (same build as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 1.0.139 | NO | >= 1.0.135 |
| 2.2.4 | 2.2.x | v0.4.12 | 1.0.139 | NO | >= 1.0.135 |

**Result**: All 5 versions in the 2.2.x stream ship serde_json >= 1.0.135. None are affected.

## Cross-check: 2.1.x Stream

For thoroughness, also checked the 2.1.x stream:

| Version | Stream | Build Tag | serde_json | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 1.0.137 | NO | >= 1.0.135 |
| 2.1.1 | 2.1.x | v0.3.12 | 1.0.137 | NO | >= 1.0.135 |

**Result**: Both versions in the 2.1.x stream also ship serde_json >= 1.0.135. None are affected.

## Summary

No supported version across any stream ships a vulnerable version of serde_json. The earliest serde_json version found in any build is 1.0.137 (in the 2.1.x stream), which is already above the fix threshold of 1.0.135.
