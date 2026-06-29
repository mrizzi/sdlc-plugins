# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | fixed version |

## Dependency Chain Context

Dependency chain for quinn-proto (Cargo):
- Ecosystem: Cargo (Rust crate)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- Source repository: rhtpa-backend

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Status |
|--------|-----------|-----------------|------------|
| 2.1.x | Cargo | release/0.3.z | Unknown -- requires `git show` verification |
| 2.2.x | Cargo | release/0.4.z | Fixed in v0.4.11+ (quinn-proto 0.11.14) |

## Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1) -- quinn-proto 0.11.9
- **2.2.x stream**: versions 2.2.0 through 2.2.2 affected; versions 2.2.3 and 2.2.4 already ship the fix (quinn-proto 0.11.14)
- The fix was picked up starting with build v0.4.11 (version 2.2.3)
