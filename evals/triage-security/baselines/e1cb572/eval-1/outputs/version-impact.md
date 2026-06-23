# Step 2 -- Version Impact Analysis: CVE-2026-31812

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

## Dependency Chain Context

Dependency chain for quinn-proto (Cargo ecosystem):
- Ecosystem: Cargo (Rust crate)
- Lock file: `Cargo.lock`
- Source repository: rhtpa-backend

quinn-proto is a QUIC protocol implementation crate. It is present across both streams (2.1.x and 2.2.x) in all versions checked. Versions 2.2.3+ (build tag v0.4.11+) ship the fixed version 0.11.14.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Available? | Notes |
|--------|-----------|-----------------|----------------|-------|
| 2.1.x | Cargo | release/0.3.z | Unknown | Lock file at latest tag (v0.3.12) shows 0.11.9 -- fix not yet on this branch |
| 2.2.x | Cargo | release/0.4.z | YES | Lock file at v0.4.11+ shows 0.11.14 -- fix already on this branch |

The 2.2.x stream already has the fix in later versions (2.2.3+). The upstream branch `release/0.4.z` already contains the updated dependency. For the 2.1.x stream, the fix has not yet been applied to the `release/0.3.z` branch.

## Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1). Fix not yet on upstream branch.
- **2.2.x stream**: versions 2.2.0, 2.2.1, 2.2.2 affected; versions 2.2.3, 2.2.4 already ship the fix.
