# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

Fix threshold: quinn-proto >= 0.11.14

| Version | Stream | Build Tag | quinn-proto version | Affected? | Notes |
|---------|--------|-----------|---------------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | < 0.11.14 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 2.2.x | v0.4.9 | (retag of v0.4.8) | YES | same as 2.2.1 |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

## Dependency Chain Context

Dependency chain for quinn-proto (Cargo):
- Ecosystem: Cargo (Rust crate)
- Lock file: Cargo.lock
- The vulnerable dependency quinn-proto is a Rust crate shipped in the backend component.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Tag at Branch Tip | quinn-proto at Tip | Fixed? |
|--------|-----------|-----------------|-------------------|--------------------|--------|
| 2.1.x | Cargo | release/0.3.z | v0.3.12 | 0.11.9 | NO |
| 2.2.x | Cargo | release/0.4.z | v0.4.12 | 0.11.14 | YES |

## Summary

- **2.1.x stream**: All versions (2.1.0, 2.1.1) are affected. Upstream branch `release/0.3.z` is NOT fixed (still on 0.11.9).
- **2.2.x stream**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 are NOT affected (ship quinn-proto 0.11.14, which is the fix version). Upstream branch `release/0.4.z` IS fixed (0.11.14 at tip).
