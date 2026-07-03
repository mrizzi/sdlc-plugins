# Step 2 -- Version Impact Analysis

## Enriched Fix Threshold

Using cross-validated fix threshold from Step 1.5: **h2 < 0.4.8** (affected), **h2 >= 0.4.8** (not affected).

## Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

### Stream 2.2.x (scoped stream -- issue TC-8030)

| Version | h2 version | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.2.0 | 0.4.8 | NO | ships fixed version |
| 2.2.1 | 0.4.8 | NO | ships fixed version |
| 2.2.2 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.9 | NO | ships version above fix threshold |
| 2.2.4 | 0.4.9 | NO | ships version above fix threshold |

### Stream 2.1.x (cross-stream)

| Version | h2 version | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.1.0 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.1.1 | 0.4.5 | YES | 0.4.5 < 0.4.8 |

## Summary

- **Scoped stream (2.2.x)**: **0 of 5 versions affected.** All versions in the 2.2.x stream ship h2 >= 0.4.8 (the fix threshold). The earliest version (2.2.0) already ships h2 0.4.8 which is the exact fix version.
- **Cross-stream (2.1.x)**: **2 of 2 versions affected.** All versions in the 2.1.x stream ship h2 0.4.5, which is below the 0.4.8 fix threshold.

## Dependency Chain Context

Dependency chain for h2:
- Ecosystem: Cargo (Rust crate)
- h2 is a Cargo dependency found in `Cargo.lock`
- Upstream branch for 2.2.x: `release/0.4.z`
- Upstream branch for 2.1.x: `release/0.3.z`

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.2.x | Cargo | release/0.4.z | All shipped versions already at or above fix threshold |
| 2.1.x | Cargo | release/0.3.z | All shipped versions (h2 0.4.5) are below fix threshold 0.4.8 |

## Triage Determination

- **Scoped stream (2.2.x)**: NOT AFFECTED -- no remediation needed within scope of TC-8030
- **Cross-stream (2.1.x)**: AFFECTED -- all versions ship vulnerable h2 0.4.5; remediation required
- This is a combination of **Case C** (scoped stream not affected) and **Case B** (cross-stream impact detected on 2.1.x)
