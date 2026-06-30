# Version Impact Analysis -- CVE-2026-28940

## Vulnerability Summary

- **Library**: serde_json
- **Affected range**: versions before 1.0.135
- **Fixed version**: 1.0.135

## Supportability Matrix (aggregated from all streams)

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | Backend Tag |
|---------|-------|------------|-------------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | Backend Tag |
|---------|-------|------------|-------------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 (retag of 2.2.1) |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 |

## Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Version | Stream | serde_json version | Affected? | Notes |
|---------|--------|--------------------|-----------|-------|
| 2.1.0 | 2.1.x | 1.0.137 | NO | >= 1.0.135 (fixed) |
| 2.1.1 | 2.1.x | 1.0.137 | NO | >= 1.0.135 (fixed) |
| 2.2.0 | 2.2.x | 1.0.138 | NO | >= 1.0.135 (fixed) |
| 2.2.1 | 2.2.x | 1.0.138 | NO | >= 1.0.135 (fixed) |
| 2.2.2 | 2.2.x | 1.0.138 | NO | retag of 2.2.1, same as 2.2.1 |
| 2.2.3 | 2.2.x | 1.0.139 | NO | >= 1.0.135 (fixed) |
| 2.2.4 | 2.2.x | 1.0.139 | NO | >= 1.0.135 (fixed) |

## Analysis

**No supported version ships a vulnerable version of serde_json.** Every version across both streams (2.1.x and 2.2.x) ships serde_json >= 1.0.135:

- Stream 2.1.x ships serde_json **1.0.137** (all versions)
- Stream 2.2.x ships serde_json **1.0.138** (2.2.0--2.2.2) or **1.0.139** (2.2.3--2.2.4)

All shipped versions are at or above the fix threshold of 1.0.135. The vulnerability (stack overflow on deeply nested input, fixed by a configurable recursion limit in 1.0.135) does not affect any supported product version.
