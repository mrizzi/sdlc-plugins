# Step 2 -- Version Impact Analysis: TC-8004

## Version Impact for CVE-2026-33501 (h2 < 0.4.8)

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | YES | < 0.4.8 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | YES | < 0.4.8 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | >= 0.4.8 (fixed version) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | >= 0.4.8 |
| 2.2.2 | 2.2.x | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | >= 0.4.8 |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | >= 0.4.8 |

## Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1 both ship h2 0.4.5)
- **2.2.x stream**: NO versions affected (all ship h2 >= 0.4.8, the fixed version)

This is a **mixed impact** scenario: the vulnerability affects the 2.1.x stream but not the 2.2.x stream.

## Dependency Chain Context

Dependency chain for h2 (Cargo):
- backend (workspace) ships h2 as a dependency in the Cargo.lock
- h2 is an HTTP/2 protocol implementation used by HTTP client/server stacks
- Profile: production (h2 is a runtime dependency)

Stream-level difference:
- **2.1.x** (v0.3.8, v0.3.12): ships h2 0.4.5 -- vulnerable
- **2.2.x** (v0.4.5+): ships h2 >= 0.4.8 -- already fixed

The 2.2.x stream picked up the h2 fix starting from its first release (2.2.0 / build v0.4.5), so the fix was incorporated before the 2.2.x stream ever shipped a vulnerable version.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | Needs fix -- h2 must be bumped from 0.4.5 to >= 0.4.8 |
| 2.2.x | Cargo | release/0.4.z | Already fixed -- h2 >= 0.4.8 shipped since 2.2.0 |
