# Step 2 -- Version Impact Analysis: CVE-2026-48901 (h2)

## Fix Threshold

Enriched fix threshold from Step 1.5: **h2 < 0.4.8** (affected), **h2 >= 0.4.8** (not affected)

Source: MITRE CVE API and OSV.dev (cross-validated, in agreement)

## Scoped Stream: 2.2.x (rhtpa-release.0.4.z)

The issue TC-8030 is scoped to the **2.2.x** stream via the summary suffix `[rhtpa-2.2]`.

### Version Impact Table (2.2.x stream)

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.1 | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.4 | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

**Result**: Only version **2.2.0** is affected in the scoped 2.2.x stream. Versions 2.2.1 and later ship h2 >= 0.4.8 and are not affected.

### Cross-Stream Impact (2.1.x stream -- outside scope)

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.1 | v0.3.12 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |

**Cross-stream impact**: All versions in the 2.1.x stream are affected. The 2.1.x stream ships h2 0.4.5, which is below the fix threshold of 0.4.8.

## Dependency Chain Context

```
Dependency chain for h2:
  Ecosystem: Cargo (Rust crate)
  Lock file: Cargo.lock
  h2 is a dependency in the backend workspace

  Affected in 2.2.0 (v0.4.5): h2 0.4.5
  Fixed from 2.2.1 (v0.4.8): h2 0.4.8
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Status |
|--------|-----------|-----------------|------------|
| 2.2.x | Cargo | release/0.4.z | Fixed (h2 >= 0.4.8 already in 2.2.1+) |
| 2.1.x | Cargo | release/0.3.z | Not fixed (h2 0.4.5 still at latest) |

## Summary

- **Scoped stream (2.2.x)**: Only 2.2.0 is affected. The fix was already picked up in 2.2.1 (h2 bumped to 0.4.8).
- **Cross-stream (2.1.x)**: All versions (2.1.0, 2.1.1) are affected. h2 remains at 0.4.5 across the entire 2.1.x stream.
