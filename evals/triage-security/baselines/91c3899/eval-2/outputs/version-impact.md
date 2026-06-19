# Step 2 -- Version Impact Analysis: TC-8002 (CVE-2026-28940)

## CVE Parameters

- **Vulnerable library**: serde_json
- **Affected range**: < 1.0.135
- **Fixed version**: 1.0.135
- **Ecosystem**: Cargo (Rust)
- **Lock file**: `Cargo.lock`

## Stream Scope

Issue is scoped to **2.2.x** stream (from summary suffix `[rhtpa-2.2]`).

Only the 2.2.x stream versions are within scope for triage decisions. The 2.1.x stream data is included for cross-stream awareness but is not in scope for this issue.

## Version Impact Table -- 2.2.x Stream (In Scope)

| Product Version | Build | Backend Tag | serde_json Version | Affected Range (< 1.0.135) | Impact |
|-----------------|-------|-------------|--------------------|-----------------------------|--------|
| 2.2.0 | 0.4.5 | `v0.4.5` | **1.0.138** | 1.0.138 >= 1.0.135 | **NO** (not affected) |
| 2.2.1 | 0.4.8 | `v0.4.8` | **1.0.138** | 1.0.138 >= 1.0.135 | **NO** (not affected) |
| 2.2.2 | 0.4.9 | `v0.4.8` | **1.0.138** | 1.0.138 >= 1.0.135 (same as 2.2.1 -- retag) | **NO** (not affected) |
| 2.2.3 | 0.4.11 | `v0.4.11` | **1.0.139** | 1.0.139 >= 1.0.135 | **NO** (not affected) |
| 2.2.4 | 0.4.12 | `v0.4.12` | **1.0.139** | 1.0.139 >= 1.0.135 | **NO** (not affected) |

## Version Impact Table -- 2.1.x Stream (Out of Scope, for reference)

| Product Version | Build | Backend Tag | serde_json Version | Affected Range (< 1.0.135) | Impact |
|-----------------|-------|-------------|--------------------|-----------------------------|--------|
| 2.1.0 | 0.3.8 | `v0.3.8` | **1.0.137** | 1.0.137 >= 1.0.135 | **NO** (not affected) |
| 2.1.1 | 0.3.12 | `v0.3.12` | **1.0.137** | 1.0.137 >= 1.0.135 | **NO** (not affected) |

## Impact Summary

**No supported versions are affected.** All versions across both streams ship serde_json >= 1.0.135, which is at or above the fixed version.

- **2.2.x stream (in scope)**: All 5 versions (2.2.0 through 2.2.4) ship serde_json 1.0.138 or 1.0.139. The lowest version shipped is **1.0.138**, which is above the fix threshold of 1.0.135.
- **2.1.x stream (out of scope)**: Both versions (2.1.0 and 2.1.1) ship serde_json 1.0.137, also above the fix threshold.

### Retag Note

Version 2.2.2 (build 0.4.9, tag `v0.4.9`) is a retag of 2.2.1 (build 0.4.8, tag `v0.4.8`). Lock file check was skipped and the result carried forward from 2.2.1: serde_json 1.0.138, NOT affected.

## Conclusion

**Zero versions affected.** This is a Step 7 Case C scenario (no supported versions affected). The issue should be closed as Not a Bug.
