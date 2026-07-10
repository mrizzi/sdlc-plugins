# Step 2 — Version Impact Analysis for CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Summary

- **Stream 2.1.x**: ALL versions affected (2.1.0, 2.1.1) — quinn-proto 0.11.9 < 0.11.14
- **Stream 2.2.x**: Versions 2.2.0, 2.2.1, 2.2.2 affected; versions 2.2.3+ ship the fix (quinn-proto 0.11.14)

## Dependency Chain Context

Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Ecosystem: Cargo
  Lock file: Cargo.lock
  Fix threshold: >= 0.11.14

The fix was introduced in build tag v0.4.11 (product version 2.2.3), meaning versions 2.2.3 and later already ship the patched quinn-proto.
