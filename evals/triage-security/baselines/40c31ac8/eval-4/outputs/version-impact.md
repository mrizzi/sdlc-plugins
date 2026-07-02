# Version Impact Analysis -- TC-8004

## CVE-2026-33501 (h2 < 0.4.8)

### Version Impact Table

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | **YES** | < 0.4.8 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | **YES** | < 0.4.8 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | >= 0.4.8 (fixed) |
| 2.2.2 | 2.2.x | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | >= 0.4.8 (fixed) |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | >= 0.4.8 (fixed) |

### Stream-Level Summary

| Stream | Affected? | Details |
|--------|-----------|---------|
| 2.1.x | **YES** | All versions (2.1.0, 2.1.1) ship h2 0.4.5, which is vulnerable |
| 2.2.x | NO | All versions ship h2 >= 0.4.8, which includes the fix |

### Mixed Impact Assessment

This vulnerability has **mixed impact across streams**:
- The **2.1.x stream** is affected -- all released versions ship h2 0.4.5, which is below the fix threshold of 0.4.8.
- The **2.2.x stream** is NOT affected -- all released versions (starting from 2.2.0) ship h2 0.4.8 or later, which includes the fix for CVE-2026-33501.

### Dependency Chain Context

```
Dependency chain for h2 (Cargo):
  Ecosystem: Cargo (Rust crate)
  Lock file: Cargo.lock
  h2 is a transitive dependency of the backend service (likely via hyper/reqwest HTTP stack)

  Stream 2.1.x: h2 0.4.5 present in Cargo.lock at tags v0.3.8 and v0.3.12
  Stream 2.2.x: h2 0.4.8+ present in Cargo.lock starting from tag v0.4.5

  The fix was picked up in the 2.2.x stream from the first release (2.2.0).
  The 2.1.x stream has not received the fix in any released version.
```

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Status |
|--------|-----------|-----------------|------------|
| 2.1.x | Cargo | release/0.3.z | Unknown -- requires `git show release/0.3.z:Cargo.lock` inspection |
| 2.2.x | Cargo | release/0.4.z | FIXED -- shipped versions already include h2 >= 0.4.8 |
