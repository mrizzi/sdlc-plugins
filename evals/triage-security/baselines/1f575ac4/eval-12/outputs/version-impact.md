# Step 2 -- Version Impact Analysis: CVE-2026-48901

## Enriched Fix Threshold

From Step 1.5 cross-validation: **h2 < 0.4.8 is affected** (MITRE and OSV.dev agree).

## Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

### Stream 2.2.x (issue-scoped stream)

| Version | Build | h2 version | Affected? | Notes |
|---------|-------|------------|-----------|-------|
| 2.2.0 | 0.4.5 | 0.4.5 | **YES** | h2 0.4.5 < 0.4.8 |
| 2.2.1 | 0.4.8 | 0.4.8 | NO | h2 0.4.8 >= 0.4.8 (fix threshold) |
| 2.2.2 | 0.4.9 | 0.4.8 | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.11 | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 |
| 2.2.4 | 0.4.12 | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 |

### Stream 2.1.x (cross-stream check)

| Version | Build | h2 version | Affected? | Notes |
|---------|-------|------------|-----------|-------|
| 2.1.0 | 0.3.8 | 0.4.5 | **YES** | h2 0.4.5 < 0.4.8 |
| 2.1.1 | 0.3.12 | 0.4.5 | **YES** | h2 0.4.5 < 0.4.8 |

## Dependency Chain Context

```
Dependency chain for h2 (Cargo):
  Ecosystem: Cargo (crates.io)
  Lock file: Cargo.lock
  h2 is a Rust crate used for HTTP/2 protocol support.
  
  Affected in 2.2.0 (build v0.4.5): h2 0.4.5
  Fixed starting from 2.2.1 (build v0.4.8): h2 bumped to 0.4.8
  
  The fix was picked up in build v0.4.8, which ships with product version 2.2.1.
  All subsequent builds (v0.4.9, v0.4.11, v0.4.12) include h2 >= 0.4.8.
```

## Impact Summary

### Scoped stream (2.2.x)

- **1 version affected**: 2.2.0 (ships h2 0.4.5)
- **4 versions not affected**: 2.2.1 through 2.2.4 (ship h2 >= 0.4.8)
- The fix was already picked up in build v0.4.8 (product version 2.2.1, released 2026-02-05)

### Cross-stream impact (2.1.x)

- **All versions affected**: 2.1.0 and 2.1.1 both ship h2 0.4.5
- This stream does not have a build that includes the fix (latest build v0.3.12 ships h2 0.4.5)

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.2.x | Cargo | release/0.4.z | Fix already present in released builds >= v0.4.8 |
| 2.1.x | Cargo | release/0.3.z | Fix NOT present in any released build; latest (v0.3.12) ships h2 0.4.5 |

## Conclusion

For the scoped stream (2.2.x): only version 2.2.0 is affected. Versions 2.2.1 and later already include the fix. Since only an older version (2.2.0) is affected and the fix is already present in current versions (2.2.1+), the scoped stream has already been remediated through normal dependency updates.

Cross-stream impact: the 2.1.x stream is fully affected (both 2.1.0 and 2.1.1 ship vulnerable h2 0.4.5). This should be flagged for cross-stream attention.
