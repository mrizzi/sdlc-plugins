# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-33501 (h2 versions before 0.4.8)

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.4.5 | YES | h2 0.4.5 < 0.4.8 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.4.5 | YES | h2 0.4.5 < 0.4.8 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.4.8 | NO | h2 0.4.8 >= 0.4.8 (fixed version) |
| 2.2.1 | 2.2.x | v0.4.8 | 0.4.8 | NO | h2 0.4.8 >= 0.4.8 |
| 2.2.2 | 2.2.x | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 |
| 2.2.4 | 2.2.x | v0.4.12 | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 |

## Stream Impact Summary

| Stream | Affected? | Details |
|--------|-----------|---------|
| 2.1.x | YES | All versions (2.1.0, 2.1.1) ship h2 0.4.5, which is vulnerable |
| 2.2.x | NO | All versions ship h2 >= 0.4.8, which includes the fix |

**Mixed impact**: The 2.1.x stream is affected while the 2.2.x stream already ships the patched version of h2.

## Dependency Chain Context (Step 2.3.5)

Dependency chain for h2 (Cargo ecosystem):

The h2 crate is a Rust HTTP/2 implementation used as a transitive dependency. The typical dependency path in the backend service is:

```
backend (workspace) -> hyper -> h2
```

- **Type**: Transitive dependency (h2 is pulled in via hyper, not declared directly)
- **Profile**: Production (hyper is a runtime HTTP dependency, not dev-only)
- **Stream 2.1.x**: Ships h2 0.4.5 across all versions (v0.3.8 and v0.3.12)
- **Stream 2.2.x**: Ships h2 >= 0.4.8 starting from the first version (v0.4.5), indicating the upstream dependency was bumped before the 2.2.0 release

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | Needs verification -- the branch may or may not have been updated with the h2 fix |
| 2.2.x | Cargo | release/0.4.z | Already ships fixed h2 >= 0.4.8 in all versions |

The upstream fix PR is [hyperium/h2#812](https://github.com/hyperium/h2/pull/812). For the 2.1.x stream, remediation requires bumping h2 to >= 0.4.8 on the `release/0.3.z` branch of the backend repository.
