# Step 2 -- Version Impact Analysis

## Enriched Fix Threshold

From Step 1.5 cross-validation: h2 versions **< 0.4.8** are affected. Fix threshold: **>= 0.4.8**.

## Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

### Stream 2.2.x (scoped stream -- issue TC-8030)

| Version | Build | Backend Tag | h2 version | Affected? | Notes |
|---------|-------|-------------|------------|-----------|-------|
| 2.2.0 | 0.4.5 | v0.4.5 | 0.4.8 | NO | ships fixed version |
| 2.2.1 | 0.4.8 | v0.4.8 | 0.4.8 | NO | ships fixed version |
| 2.2.2 | 0.4.9 | v0.4.8 | 0.4.8 | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.11 | v0.4.11 | 0.4.9 | NO | ships version above fix threshold |
| 2.2.4 | 0.4.12 | v0.4.12 | 0.4.9 | NO | ships version above fix threshold |

**Result: No versions in the 2.2.x stream are affected.** All versions ship h2 >= 0.4.8.

### Stream 2.1.x (cross-stream analysis)

| Version | Build | Backend Tag | h2 version | Affected? | Notes |
|---------|-------|-------------|------------|-----------|-------|
| 2.1.0 | 0.3.8 | v0.3.8 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.1.1 | 0.3.12 | v0.3.12 | 0.4.5 | YES | 0.4.5 < 0.4.8 |

**Result: All versions in the 2.1.x stream are affected.** Both versions ship h2 0.4.5, which is below the fix threshold of 0.4.8.

## Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> h2
  Ecosystem: Cargo (crates.io)
  Lock file: Cargo.lock
  Type: direct or transitive dependency (requires lock file inspection for full chain)
  Profile: production (h2 is an HTTP/2 protocol implementation, runtime dependency)
```

## Cross-Stream Summary

| Stream | Versions Affected | Versions Not Affected |
|--------|-------------------|-----------------------|
| 2.2.x (scoped) | 0 of 5 | 5 of 5 |
| 2.1.x (cross-stream) | 2 of 2 | 0 of 2 |

## Triage Outcome

**Scoped stream (2.2.x)**: No supported versions in the 2.2.x stream ship a vulnerable version of h2. All versions ship h2 >= 0.4.8, which is at or above the fix threshold.

**Cross-stream impact (2.1.x)**: All versions in the 2.1.x stream ship h2 0.4.5, which is affected (below fix threshold 0.4.8). This stream is outside the scope of TC-8030 but requires attention.

**Recommendation**: Case C -- Close TC-8030 as Not a Bug (not affected) for the 2.2.x stream. Post cross-stream impact comment noting 2.1.x is affected.
