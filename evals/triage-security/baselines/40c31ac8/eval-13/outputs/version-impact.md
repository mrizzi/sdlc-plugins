# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Dependency Chain Context

Dependency chain for quinn-proto (Cargo):

- quinn-proto is a Cargo (Rust) dependency found in `Cargo.lock` at the pinned source commits for the `backend` repository.
- The library is part of the QUIC networking stack. Typical dependency path: `backend (workspace) -> quinn -> quinn-proto`.
- Profile: production (quinn is a runtime networking dependency).
- First appeared: present in all versions checked (2.1.0 through 2.2.4).
- The dependency was updated from 0.11.9 to 0.11.12 between versions 2.2.0 and 2.2.1, and then to 0.11.14 (the fix) between versions 2.2.2 and 2.2.3.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | (not checked -- mock data does not include branch HEAD) | Unknown |
| 2.2.x | Cargo | release/0.4.z | (not checked -- mock data does not include branch HEAD) | Unknown |

Note: Since version 2.2.3 (build 0.4.11) and 2.2.4 (build 0.4.12) already ship the fixed version 0.11.14, the upstream fix for the 2.2.x stream has been incorporated in released builds. The upstream branch `release/0.4.z` likely already contains the fix at HEAD.

For the 2.1.x stream, the latest released version (2.1.1, build 0.3.12) ships quinn-proto 0.11.9, indicating the upstream branch `release/0.3.z` has not yet picked up the fix.

## Affects Versions Correction (Step 3)

**Issue is scoped to stream 2.2.x** (per summary suffix `[rhtpa-2.2]`).

Current Affects Versions: `[RHTPA 2.0.0]`
Proposed Affects Versions (scoped to 2.2.x affected versions): `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

The PSIRT-assigned version `RHTPA 2.0.0` is incorrect -- there is no 2.0.x stream in the configured Version Streams. The lock file analysis shows versions 2.2.0, 2.2.1, and 2.2.2 ship vulnerable quinn-proto versions (< 0.11.14). Versions 2.2.3 and 2.2.4 ship the fixed version and are not affected.

## Cross-Stream Impact (Case B)

Stream 2.1.x is **also affected** but outside this issue's scope:
- 2.1.0 ships quinn-proto 0.11.9 (affected)
- 2.1.1 ships quinn-proto 0.11.9 (affected)

This will be addressed via Case B proactive remediation (preemptive tasks) if no sibling CVE Jira exists for stream 2.1.x.
