# Step 2 -- Version Impact Analysis: CVE-2026-28940

## Version Impact Table

CVE-2026-28940 affects serde_json versions before 1.0.135. The fix version is 1.0.135.

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | serde_json version | Affected? | Notes |
|---------|-----------|--------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 1.0.137 | NO | Ships fixed version (>= 1.0.135) |
| 2.1.1 | v0.3.12 | 1.0.137 | NO | Ships fixed version (>= 1.0.135) |

### Stream 2.2.x (rhtpa-release.0.4.z) -- Issue scope

| Version | Build Tag | serde_json version | Affected? | Notes |
|---------|-----------|--------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 1.0.138 | NO | Ships fixed version (>= 1.0.135) |
| 2.2.1 | v0.4.8 | 1.0.138 | NO | Ships fixed version (>= 1.0.135) |
| 2.2.2 | v0.4.9 | -- | NO | Retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 1.0.139 | NO | Ships fixed version (>= 1.0.135) |
| 2.2.4 | v0.4.12 | 1.0.139 | NO | Ships fixed version (>= 1.0.135) |

### Combined Version Impact Table

| Version | Stream | serde_json | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 1.0.137 | NO | |
| 2.1.1 | 2.1.x | 1.0.137 | NO | |
| 2.2.0 | 2.2.x | 1.0.138 | NO | |
| 2.2.1 | 2.2.x | 1.0.138 | NO | |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 1.0.139 | NO | |
| 2.2.4 | 2.2.x | 1.0.139 | NO | |

## Analysis Summary

**No supported versions are affected.** Every version across both streams ships serde_json >= 1.0.135, which is at or above the fix threshold. The earliest version shipped (2.1.0, build v0.3.8) already includes serde_json 1.0.137, which is 2 patch versions ahead of the fix.

- Minimum serde_json version across all versions: **1.0.137** (streams 2.1.x)
- Maximum serde_json version across all versions: **1.0.139** (stream 2.2.x, builds v0.4.11+)
- Fix threshold: **1.0.135**
- All shipped versions exceed the fix threshold.
