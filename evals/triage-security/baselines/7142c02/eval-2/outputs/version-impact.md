# Step 2 -- Version Impact Analysis for CVE-2026-28940

## Fix Threshold

- **Vulnerable range**: serde_json versions before 1.0.135
- **Fixed version**: 1.0.135
- Any version >= 1.0.135 is NOT affected.

## Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | serde_json version | Affected? | Notes |
|---------|-------|--------------------|-----------|-------|
| 2.1.0 | 0.3.8 | 1.0.137 | NO | >= 1.0.135 fix threshold |
| 2.1.1 | 0.3.12 | 1.0.137 | NO | >= 1.0.135 fix threshold |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | serde_json version | Affected? | Notes |
|---------|-------|--------------------|-----------|-------|
| 2.2.0 | 0.4.5 | 1.0.138 | NO | >= 1.0.135 fix threshold |
| 2.2.1 | 0.4.8 | 1.0.138 | NO | >= 1.0.135 fix threshold |
| 2.2.2 | 0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.11 | 1.0.139 | NO | >= 1.0.135 fix threshold |
| 2.2.4 | 0.4.12 | 1.0.139 | NO | >= 1.0.135 fix threshold |

### Combined Summary

| Version | serde_json | Affected? |
|---------|------------|-----------|
| 2.1.0 | 1.0.137 | NO |
| 2.1.1 | 1.0.137 | NO |
| 2.2.0 | 1.0.138 | NO |
| 2.2.1 | 1.0.138 | NO |
| 2.2.2 | -- | NO (retag of 2.2.1) |
| 2.2.3 | 1.0.139 | NO |
| 2.2.4 | 1.0.139 | NO |

**Result: NO supported versions are affected.** Every version across both streams
ships serde_json >= 1.0.137, which is well above the fix threshold of 1.0.135.

The lowest serde_json version found across all streams is **1.0.137** (in 2.1.0 and
2.1.1), which is still 2 patch versions above the fix (1.0.135).
