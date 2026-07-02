# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Dependency Chain for quinn-proto

```
Dependency chain for quinn-proto (Cargo):
  Ecosystem: Cargo (Rust crate)
  Lock file: Cargo.lock
  Repository: backend
  Check command: git show <tag>:Cargo.lock

  First affected: 2.1.0 (tag v0.3.8, quinn-proto 0.11.9)
  Last affected: 2.2.2 (retag of v0.4.8, quinn-proto 0.11.12)
  Fixed from: 2.2.3 (tag v0.4.11, quinn-proto 0.11.14)
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Status |
|--------|-----------|-----------------|------------|
| 2.1.x | Cargo | release/0.3.z | Needs upstream backport |
| 2.2.x | Cargo | release/0.4.z | Fixed (quinn-proto >= 0.11.14 at v0.4.11+) |

## Summary

- **Stream 2.2.x (issue scope)**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fix (quinn-proto 0.11.14).
- **Stream 2.1.x (cross-stream)**: All versions (2.1.0, 2.1.1) are affected, shipping quinn-proto 0.11.9.
