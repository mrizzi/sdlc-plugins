# Step 2 -- Version Impact Analysis for TC-8001

## CVE Details

- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Affected range**: versions before 0.11.14 (< 0.11.14)
- **Fixed version**: 0.11.14
- **Ecosystem**: Cargo (lock file: `Cargo.lock`)

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build Tag | quinn-proto version | Affected? | Notes |
|---------|--------|-----------|---------------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | **YES** | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | **YES** | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | **YES** | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | **YES** | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | **YES** | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | at fix threshold |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | at fix threshold |

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (present in Cargo.lock)
  Profile: production (quinn-proto is a runtime QUIC protocol dependency)
  Ecosystem: Cargo

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml / Cargo.lock
```

## Stream Impact Summary

### 2.2.x stream (issue scope -- `[rhtpa-2.2]`)

- **Affected versions**: 2.2.0, 2.2.1, 2.2.2
- **Not affected**: 2.2.3 (fixed at 0.11.14), 2.2.4 (fixed at 0.11.14)
- The fix was introduced in build v0.4.11 (version 2.2.3)

### 2.1.x stream (outside issue scope -- cross-stream impact)

- **Affected versions**: 2.1.0, 2.1.1
- Both versions ship quinn-proto 0.11.9, which is vulnerable
- This stream is outside the issue's `[rhtpa-2.2]` scope and would be tracked via Case B cross-stream impact

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Status |
|--------|-----------|-----------------|------------|
| 2.2.x | Cargo | release/0.4.z | **FIXED** -- versions 2.2.3+ already ship 0.11.14 |
| 2.1.x | Cargo | release/0.3.z | **NOT FIXED** -- latest (v0.3.12) ships 0.11.9 |

## Affects Versions Correction (Step 3 preview)

The PSIRT-assigned Affects Versions is `RHTPA 2.0.0`, which does not match any configured version stream. Based on lock file analysis, scoped to the 2.2.x stream:

- **Current**: [RHTPA 2.0.0]
- **Proposed**: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

RHTPA 2.2.3 and RHTPA 2.2.4 are NOT affected (ship quinn-proto 0.11.14, which is at or above the fix threshold).
