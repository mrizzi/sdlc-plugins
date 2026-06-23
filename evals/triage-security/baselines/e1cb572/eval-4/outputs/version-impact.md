# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-33501 (h2 < 0.4.8)

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | **YES** | ships vulnerable h2 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | **YES** | ships vulnerable h2 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | ships fixed version |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | ships fixed version |
| 2.2.2 | 2.2.x | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | ships version above fix threshold |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | ships version above fix threshold |

## Stream Summary

| Stream | Affected Versions | Status |
|--------|-------------------|--------|
| 2.1.x | 2.1.0, 2.1.1 | **AFFECTED** -- all versions ship h2 0.4.5 (vulnerable) |
| 2.2.x | _(none)_ | NOT AFFECTED -- all versions ship h2 >= 0.4.8 (fixed) |

## Dependency Chain Context

The h2 crate is a Cargo (Rust) dependency in the backend repository. Based on lock file analysis:

- **Ecosystem**: Cargo
- **Lock file**: `Cargo.lock`
- **Dependency type**: h2 is a transitive dependency commonly pulled in via HTTP client/server crates (e.g., hyper, reqwest, tonic)
- **Stream divergence**: The 2.1.x stream pins backend at v0.3.x tags which bundle h2 0.4.5. The 2.2.x stream pins backend at v0.4.x tags which bundle h2 >= 0.4.8 (the fixed version). The fix was picked up organically during the v0.4.5 backend release that ships with 2.2.0.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.1.x | Cargo | release/0.3.z | Needs h2 bump to >= 0.4.8 |
| 2.2.x | Cargo | release/0.4.z | Already ships h2 >= 0.4.8 -- no action needed |

The upstream fix ([hyperium/h2#812](https://github.com/hyperium/h2/pull/812)) is available. The 2.1.x stream's release/0.3.z branch needs to bump h2 to >= 0.4.8. The 2.2.x stream already ships the fixed version.
