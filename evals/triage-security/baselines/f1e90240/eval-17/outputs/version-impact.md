# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | Backend Tag | quinn-proto | Affected? | Notes |
|---------|-------|------------|-------------|-------------|-----------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | 0.11.9 | **YES** | < 0.11.14 |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | 0.11.9 | **YES** | < 0.11.14 |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | Backend Tag | quinn-proto | Affected? | Notes |
|---------|-------|------------|-------------|-------------|-----------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | 0.11.9 | **YES** | < 0.11.14 |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | 0.11.12 | **YES** | < 0.11.14 |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | 0.11.12 | **YES** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | 0.11.14 | **NO** | >= 0.11.14 (fixed) |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | 0.11.14 | **NO** | >= 0.11.14 (fixed) |

### Combined Version Impact Table

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | **YES** | |
| 2.1.1 | 0.11.9 | **YES** | |
| 2.2.0 | 0.11.9 | **YES** | |
| 2.2.1 | 0.11.12 | **YES** | |
| 2.2.2 | 0.11.12 | **YES** | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | fixed |
| 2.2.4 | 0.11.14 | NO | fixed |

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (Cargo ecosystem)
  Lock file: Cargo.lock
  Profile: production (quinn-proto is a runtime QUIC dependency)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Check Command | Notes |
|--------|-----------|-----------------|---------------|-------|
| 2.1.x | Cargo | `release/0.3.z` | `git show release/0.3.z:Cargo.lock` | Check branch HEAD for fix status |
| 2.2.x | Cargo | `release/0.4.z` | `git show release/0.4.z:Cargo.lock` | Versions 2.2.3+ already ship 0.11.14 -- fix is on branch |

The fix is already present in the 2.2.x stream (versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14). Remediation for the 2.2.x stream affects only versions 2.2.0, 2.2.1, and 2.2.2. For the 2.1.x stream, the upstream branch `release/0.3.z` must be checked at HEAD to determine if the fix has been backported.

## Affects Versions Correction (Step 3)

- **Current Affects Versions**: RHTPA 2.0.0 (incorrect -- no 2.0.x stream exists)
- **Issue scope**: stream 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Affected versions in scope**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Proposed correction**: `[RHTPA 2.0.0]` -> `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Note: Versions 2.1.0 and 2.1.1 are also affected but belong to stream 2.1.x, which is outside this issue's scope. Cross-stream impact is handled via Case B (see remediation).
