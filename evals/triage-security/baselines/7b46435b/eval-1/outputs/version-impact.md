# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | Backend Tag | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Evidence

Lock file inspection commands used (simulated from mock data):

- `git show v0.3.8:Cargo.lock | grep -A2 'name = "quinn-proto"'` -> version 0.11.9
- `git show v0.3.12:Cargo.lock | grep -A2 'name = "quinn-proto"'` -> version 0.11.9
- `git show v0.4.5:Cargo.lock | grep -A2 'name = "quinn-proto"'` -> version 0.11.9
- `git show v0.4.8:Cargo.lock | grep -A2 'name = "quinn-proto"'` -> version 0.11.12
- v0.4.9: skipped -- retag of v0.4.8, same result (0.11.12)
- `git show v0.4.11:Cargo.lock | grep -A2 'name = "quinn-proto"'` -> version 0.11.14
- `git show v0.4.12:Cargo.lock | grep -A2 'name = "quinn-proto"'` -> version 0.11.14

## Summary

- **2.1.x stream**: All versions (2.1.0, 2.1.1) are affected -- they ship quinn-proto 0.11.9.
- **2.2.x stream**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fixed version (0.11.14) and are NOT affected.
- The fix was picked up in the 2.2.x stream starting with build v0.4.11 (version 2.2.3).
- The 2.1.x stream has NOT picked up the fix in any released version.
