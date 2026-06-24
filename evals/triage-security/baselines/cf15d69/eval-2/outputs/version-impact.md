# Step 2 -- Version Impact Analysis: CVE-2026-28940

## Vulnerability Summary

- **Library**: serde_json
- **Affected range**: < 1.0.135
- **Fix threshold**: >= 1.0.135

## Supportability Matrix (Aggregated)

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | Backend Tag |
|---------|-------|------------|-------------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | Backend Tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | |

## Dependency Version Extraction (from mock lock file data)

Lock file: `Cargo.lock`, check command: `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'`

### serde_json versions by backend tag

| Tag | serde_json version | Source |
|-----|--------------------|--------|
| v0.3.8 | 1.0.137 | Cargo.lock at v0.3.8 |
| v0.3.12 | 1.0.137 | Cargo.lock at v0.3.12 |
| v0.4.5 | 1.0.138 | Cargo.lock at v0.4.5 |
| v0.4.8 | 1.0.138 | Cargo.lock at v0.4.8 |
| v0.4.9 | (retag of v0.4.8) | same as v0.4.8 |
| v0.4.11 | 1.0.139 | Cargo.lock at v0.4.11 |
| v0.4.12 | 1.0.139 | Cargo.lock at v0.4.12 |

## Version Impact Table

CVE-2026-28940 (serde_json < 1.0.135, fix threshold >= 1.0.135):

| Version | Stream | serde_json version | Affected? | Notes |
|---------|--------|--------------------|-----------|-------|
| 2.1.0 | 2.1.x | 1.0.137 | **NO** | Ships 1.0.137 >= 1.0.135 |
| 2.1.1 | 2.1.x | 1.0.137 | **NO** | Ships 1.0.137 >= 1.0.135 |
| 2.2.0 | 2.2.x | 1.0.138 | **NO** | Ships 1.0.138 >= 1.0.135 |
| 2.2.1 | 2.2.x | 1.0.138 | **NO** | Ships 1.0.138 >= 1.0.135 |
| 2.2.2 | 2.2.x | 1.0.138 | **NO** | Retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 1.0.139 | **NO** | Ships 1.0.139 >= 1.0.135 |
| 2.2.4 | 2.2.x | 1.0.139 | **NO** | Ships 1.0.139 >= 1.0.135 |

## Key Finding

**No supported version is affected.** Every version across both streams (2.1.x and 2.2.x) ships serde_json >= 1.0.137, which is well above the fix threshold of 1.0.135. The vulnerable code (serde_json < 1.0.135) was never shipped in any supported product version.

The earliest serde_json version found in any shipped build is **1.0.137** (in both 2.1.0 and 2.1.1), which already includes the recursion limit fix introduced in 1.0.135.

## Upstream Fix Status

Not applicable -- all versions already ship fixed serde_json. No upstream remediation is needed.
