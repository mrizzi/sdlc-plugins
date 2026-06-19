# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

All versions from both supported streams (2.1.x and 2.2.x) are included.

| Version | Stream | Backend Tag | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | `v0.4.8` | 0.11.12 | YES | retag of 2.2.1 -- same as 2.2.1 |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | ships fixed version |

## Method

- **Lock file**: `Cargo.lock` at each pinned backend commit tag
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- **Retag handling**: Version 2.2.2 uses backend tag `v0.4.8` (retag of 2.2.1), so the lock file check was skipped and the result carried forward from 2.2.1.
- **Pinned commits**: All version checks used the exact tags from the supportability matrix (e.g., `v0.3.8`, `v0.3.12`, `v0.4.5`, `v0.4.8`, `v0.4.11`, `v0.4.12`), not branch HEAD.

## Dependency Chain Context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) -> quinn -> quinn-proto
  Ecosystem: Cargo (Rust crate)
  Profile: production (runtime dependency)

Present in: all versions across both streams (2.1.x and 2.2.x)
Fixed from: 2.2.3 onward (quinn-proto bumped to 0.11.14 in backend tag v0.4.11)
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.1.x | Cargo | `release/0.3.z` | Requires upstream check at branch HEAD |
| 2.2.x | Cargo | `release/0.4.z` | Fix already landed -- v0.4.11+ ships 0.11.14 |

## Cross-Stream Impact

The vulnerability affects **both** the 2.1.x and 2.2.x streams. This issue (TC-8001) is scoped to the 2.2.x stream. The 2.1.x stream is also affected (versions 2.1.0, 2.1.1 both ship quinn-proto 0.11.9) and would require a companion PSIRT issue or separate triage.
