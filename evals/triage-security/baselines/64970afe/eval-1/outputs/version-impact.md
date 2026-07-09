# Version Impact — CVE-2026-31812

## Step 2 — Version Impact Analysis

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Build Tag | quinn-proto | Affected? | Notes |
|--------|---------|-----------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | ships fixed version |

### Dependency chain context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) -> quinn-proto
  Type: to be confirmed via Cargo.toml inspection
  Profile: production (quinn-proto is a QUIC transport dependency)
  Lock file: Cargo.lock
  Check command: git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'
```

### Upstream fix status

| Stream | Ecosystem | Upstream Branch | Source Repo | Notes |
|--------|-----------|-----------------|-------------|-------|
| 2.1.x | Cargo | release/0.3.z | rhtpa-backend | Fix not yet picked up (latest tag v0.3.12 ships 0.11.9) |
| 2.2.x | Cargo | release/0.4.z | rhtpa-backend | Fix available starting at v0.4.11 (ships 0.11.14) |

### Summary

- **2.1.x stream**: All versions (2.1.0, 2.1.1) are affected. Ships quinn-proto 0.11.9.
- **2.2.x stream**: Versions 2.2.0, 2.2.1, 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fix (quinn-proto 0.11.14).
- The fix was picked up in the 2.2.x stream starting with build 0.4.11 (version 2.2.3). The 2.1.x stream has not yet received the fix.
