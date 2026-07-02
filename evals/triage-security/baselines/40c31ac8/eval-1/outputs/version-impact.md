# Step 2 -- Version Impact Analysis

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

### Analysis

- **Fix threshold:** quinn-proto >= 0.11.14 (from Jira description; cross-validated with external CVE data)
- **Affected versions:** 2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2 (all ship quinn-proto < 0.11.14)
- **Not affected:** 2.2.3, 2.2.4 (ship quinn-proto 0.11.14, which is the fixed version)
- **Retag handling:** Version 2.2.2 is a retag of 2.2.1 (build tag v0.4.9 reuses v0.4.8 backend sources), so the lock file check was skipped and the result carried forward from 2.2.1.

### Dependency Chain Context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) -> quinn -> quinn-proto
  Profile: production (runtime dependency)

Present in: all versions across both streams (2.1.x and 2.2.x)
Fixed in: 2.2.3+ (commit v0.4.11 bumped quinn-proto to 0.11.14)
```

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | quinn-proto at HEAD | Fixed? |
|--------|-----------|-----------------|---------------------|--------|
| 2.1.x | Cargo | release/0.3.z | (needs verification) | Unknown |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |

The 2.2.x upstream branch (`release/0.4.z`) already has the fix at HEAD (quinn-proto 0.11.14), as evidenced by builds v0.4.11 and v0.4.12 shipping the fixed version. The 2.1.x upstream branch (`release/0.3.z`) status would need to be verified via `git show release/0.3.z:Cargo.lock`.
