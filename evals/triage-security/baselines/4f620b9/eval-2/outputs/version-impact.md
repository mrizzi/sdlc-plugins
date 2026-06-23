# Step 2 -- Version Impact Analysis: TC-8002 (CVE-2026-28940)

## Vulnerability Threshold

- **Vulnerable library**: serde_json
- **Affected range**: versions before 1.0.135
- **Fixed version**: 1.0.135
- **Ecosystem**: Cargo (Rust crate)

A version is **affected** if it ships serde_json < 1.0.135. A version is **not affected** if it ships serde_json >= 1.0.135.

## Version Impact Table

### Stream 2.1.x (rhtpa-release.0.3.z)

| Product Version | Build | Backend Tag | serde_json Version | Affected? | Evidence |
|-----------------|-------|-------------|-------------------|-----------|----------|
| 2.1.0 | 0.3.8 | `v0.3.8` | 1.0.137 | **NO** | 1.0.137 >= 1.0.135 (fix threshold) |
| 2.1.1 | 0.3.12 | `v0.3.12` | 1.0.137 | **NO** | 1.0.137 >= 1.0.135 (fix threshold) |

### Stream 2.2.x (rhtpa-release.0.4.z) -- Issue-scoped stream

| Product Version | Build | Backend Tag | serde_json Version | Affected? | Evidence |
|-----------------|-------|-------------|-------------------|-----------|----------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 1.0.138 | **NO** | 1.0.138 >= 1.0.135 (fix threshold) |
| 2.2.1 | 0.4.8 | `v0.4.8` | 1.0.138 | **NO** | 1.0.138 >= 1.0.135 (fix threshold) |
| 2.2.2 | 0.4.9 | `v0.4.8` | 1.0.138 | **NO** | Retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 0.4.11 | `v0.4.11` | 1.0.139 | **NO** | 1.0.139 >= 1.0.135 (fix threshold) |
| 2.2.4 | 0.4.12 | `v0.4.12` | 1.0.139 | **NO** | 1.0.139 >= 1.0.135 (fix threshold) |

## Summary

| Stream | Versions Analyzed | Affected Count | Result |
|--------|-------------------|----------------|--------|
| 2.1.x | 2 | 0 | **All versions ship patched serde_json** |
| 2.2.x | 5 (including 1 retag) | 0 | **All versions ship patched serde_json** |

**Conclusion**: No supported product version ships a vulnerable version of serde_json. Every version across both the 2.1.x and 2.2.x streams ships serde_json >= 1.0.135, which includes the fix for CVE-2026-28940. The earliest version shipped (2.1.0 at tag v0.3.8) already includes serde_json 1.0.137, which is two patch versions ahead of the fix.

## Retag Handling

- **2.2.2** (build 0.4.9) is a retag of build 0.4.8 (same backend tag as 2.2.1). Lock file check was skipped; result carried forward from 2.2.1 (serde_json 1.0.138, not affected).
