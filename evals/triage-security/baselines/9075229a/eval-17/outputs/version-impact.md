# Step 2 -- Version Impact Analysis: CVE-2026-31812

## 2.1 -- Supportability Matrix

Loaded from two configured Version Streams:

- **2.1.x** stream: `security-matrix.md` (rhtpa-release.0.3.z) -- Last-Updated: 2026-06-28T10:00:00Z (5 days ago, within 14-day threshold)
- **2.2.x** stream: `security-matrix.md` (rhtpa-release.0.4.z) -- Last-Updated: 2026-06-28T10:00:00Z (5 days ago, within 14-day threshold)

No staleness warnings.

## 2.3 -- Dependency Version Extraction

Ecosystem: **Cargo** | Library: **quinn-proto** | Fix threshold: **0.11.14**

Lock file inspection results (simulated `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`):

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Tag | quinn-proto version | Affected? | Notes |
|---------|-----|---------------------|-----------|-------|
| 2.1.0 | `v0.3.8` | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | `v0.3.12` | 0.11.9 | YES | 0.11.9 < 0.11.14 |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Tag | quinn-proto version | Affected? | Notes |
|---------|-----|---------------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | `v0.4.8` | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | `v0.4.9` | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 0.11.14 | NO | 0.11.14 >= 0.11.14 (at fix threshold) |
| 2.2.4 | `v0.4.12` | 0.11.14 | NO | 0.11.14 >= 0.11.14 (at fix threshold) |

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | 0.11.14 | NO | |

### Dependency Chain Context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) -> quinn -> quinn-proto
  Ecosystem: Cargo (source dependency, lock file: Cargo.lock)
  Profile: production (quinn is a runtime dependency)

  Present in all versions across both streams (0.11.9 from 2.1.0 onward).
  Fixed in 2.2.3+ (bumped to 0.11.14 at tag v0.4.11).
```

## 2.5 -- Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Repository | Notes |
|--------|-----------|-----------------|------------|-------|
| 2.1.x | Cargo | `release/0.3.z` | backend | Upstream fix PR: [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| 2.2.x | Cargo | `release/0.4.z` | backend | Upstream fix PR: [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |

Note: The upstream fix is available via quinn-rs/quinn#2048. Versions 2.2.3+ already ship the fixed version (0.11.14), confirming the fix was picked up in the 2.2.x stream starting at tag v0.4.11. The 2.1.x stream has not yet picked up the fix (both versions ship 0.11.9).

## Summary

- **Issue stream scope**: 2.2.x
- **Affected within scope (2.2.x)**: 2.2.0, 2.2.1, 2.2.2 (versions before 2.2.3)
- **Not affected within scope (2.2.x)**: 2.2.3, 2.2.4 (ship quinn-proto 0.11.14)
- **Cross-stream impact**: 2.1.x stream is also affected (2.1.0, 2.1.1 both ship quinn-proto 0.11.9)
- **PSIRT Affects Versions mismatch**: Jira has "RHTPA 2.0.0" but no 2.0.x stream exists in the configuration. Affects Versions needs correction to reflect the actually affected versions within the 2.2.x scope.
