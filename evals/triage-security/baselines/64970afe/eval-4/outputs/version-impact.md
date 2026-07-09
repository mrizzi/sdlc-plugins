# Step 2 -- Version Impact Analysis: CVE-2026-33501

## Fix Threshold

- Vulnerable library: h2
- Affected range: versions before 0.4.8
- Fixed version: 0.4.8

## Version Impact Table

Version Impact for CVE-2026-33501 (h2 < 0.4.8):

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | YES | ships vulnerable h2 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | YES | ships vulnerable h2 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | ships fixed version |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | ships fixed version |
| 2.2.2 | 2.2.x | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | ships version above fix threshold |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | ships version above fix threshold |

## Stream Impact Summary

| Stream | Affected? | Details |
|--------|-----------|---------|
| 2.1.x | YES | All versions (2.1.0, 2.1.1) ship h2 0.4.5, which is below the fix threshold of 0.4.8 |
| 2.2.x | NO | All versions ship h2 >= 0.4.8 (the fixed version or later) |

This is a **mixed impact** scenario: the 2.1.x stream is affected while the 2.2.x stream already ships the patched version of h2.

## Dependency Chain Context

Dependency chain for h2 (Cargo):
- backend (workspace) -> h2
- Type: source dependency (Cargo crate)
- Ecosystem: Cargo
- Lock file: Cargo.lock
- Profile: production (h2 is a runtime HTTP/2 protocol dependency)

The h2 crate provides HTTP/2 protocol support for the backend service. It is present in the Cargo.lock at all pinned commits across both streams.

- In the 2.1.x stream, h2 is pinned at 0.4.5 (vulnerable)
- In the 2.2.x stream, h2 was already updated to 0.4.8+ (fixed) starting from the first version (2.2.0)

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | h2 at branch tag | Fixed? |
|--------|-----------|-----------------|------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.4.5 (at v0.3.12) | NO -- latest 2.1.x tag still ships vulnerable h2 |
| 2.2.x | Cargo | release/0.4.z | 0.4.9 (at v0.4.12) | YES -- already ships h2 >= 0.4.8 |

The upstream fix PR is available at https://github.com/hyperium/h2/pull/812. The 2.1.x stream's upstream branch (release/0.3.z) has NOT yet picked up the fix -- remediation requires a backport to bump h2 >= 0.4.8 on that branch.
