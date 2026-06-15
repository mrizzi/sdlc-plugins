# Step 2: Version Impact Analysis - TC-8002

## Vulnerability Threshold

- **Library**: serde_json
- **Affected range**: < 1.0.135
- **Fixed version**: 1.0.135
- **Determination**: Any version of serde_json >= 1.0.135 is NOT affected.

## 2.2.x Stream (Issue-Scoped - [rhtpa-2.2])

This is the stream explicitly scoped by the issue summary tag `[rhtpa-2.2]`.

| Product Version | Build | Backend Tag | serde_json Version | Affected? | Rationale |
|-----------------|-------|-------------|-------------------|-----------|-----------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 1.0.138 | NO | 1.0.138 >= 1.0.135 (patched) |
| 2.2.1 | 0.4.8 | `v0.4.8` | 1.0.138 | NO | 1.0.138 >= 1.0.135 (patched) |
| 2.2.2 | 0.4.9 | `v0.4.8` | 1.0.138 | NO | Retag of v0.4.8; carry forward 1.0.138 >= 1.0.135 |
| 2.2.3 | 0.4.11 | `v0.4.11` | 1.0.139 | NO | 1.0.139 >= 1.0.135 (patched) |
| 2.2.4 | 0.4.12 | `v0.4.12` | 1.0.139 | NO | 1.0.139 >= 1.0.135 (patched) |

**2.2.x Result**: 0 of 5 versions affected.

## 2.1.x Stream (Completeness Check)

Included for full coverage across all supported version streams.

| Product Version | Build | Backend Tag | serde_json Version | Affected? | Rationale |
|-----------------|-------|-------------|-------------------|-----------|-----------|
| 2.1.0 | 0.3.8 | `v0.3.8` | 1.0.137 | NO | 1.0.137 >= 1.0.135 (patched) |
| 2.1.1 | 0.3.12 | `v0.3.12` | 1.0.137 | NO | 1.0.137 >= 1.0.135 (patched) |

**2.1.x Result**: 0 of 2 versions affected.

## Overall Impact Summary

**ALL supported versions across ALL streams ship serde_json >= 1.0.135 and are NOT affected by CVE-2026-28940.**

No version in either the 2.1.x or 2.2.x stream ships a vulnerable version of serde_json. The lowest serde_json version found across all tags is 1.0.137 (in the 2.1.x stream), which is already above the fix threshold of 1.0.135.

| Stream | Versions Checked | Versions Affected | Min serde_json Found |
|--------|-----------------|-------------------|---------------------|
| 2.2.x | 5 | 0 | 1.0.138 |
| 2.1.x | 2 | 0 | 1.0.137 |
| **Total** | **7** | **0** | **1.0.137** |
