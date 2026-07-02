# Step 2 -- Version Impact Analysis

## Vulnerability Details

| Field | Value |
|-------|-------|
| CVE | CVE-2026-31812 |
| Library | quinn-proto |
| Affected range | < 0.11.14 |
| Fixed version | 0.11.14 |
| Ecosystem | Cargo |
| Lock file | Cargo.lock |

## Version Impact Table

### Stream 2.2.x (scoped -- issue stream)

| Product Version | Build | Backend Tag | quinn-proto Version | Affected? | Evidence |
|-----------------|-------|-------------|---------------------|-----------|----------|
| 2.2.0 | 0.4.5 | v0.4.5 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.2.1 | 0.4.8 | v0.4.8 | 0.11.12 | **YES** | 0.11.12 < 0.11.14 |
| 2.2.2 | 0.4.9 | v0.4.8 | 0.11.12 | **YES** | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 0.4.11 | v0.4.11 | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | 0.4.12 | v0.4.12 | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 (fixed) |

**Summary for 2.2.x**: Versions 2.2.0, 2.2.1, and 2.2.2 shipped with vulnerable quinn-proto (< 0.11.14). The fix landed in version 2.2.3 (build 0.4.11) which updated quinn-proto to 0.11.14. The latest version (2.2.4) also ships the fixed version. **The vulnerability is already fixed in the latest 2.2.x releases.**

### Stream 2.1.x (cross-stream)

| Product Version | Build | Backend Tag | quinn-proto Version | Affected? | Evidence |
|-----------------|-------|-------------|---------------------|-----------|----------|
| 2.1.0 | 0.3.8 | v0.3.8 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.1.1 | 0.3.12 | v0.3.12 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |

**Summary for 2.1.x**: All versions in the 2.1.x stream ship vulnerable quinn-proto 0.11.9. No version in this stream has been updated to the fixed version. **Remediation is required for the 2.1.x stream.**

## Retag Handling

Version 2.2.2 (build 0.4.9) is a retag of version 2.2.1 (build 0.4.8) -- the backend tag v0.4.8 is reused. The lock file check was skipped for 2.2.2 and the result carried forward from 2.2.1: quinn-proto 0.11.12 (affected).

## Affects Versions Correction (Preview)

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, which does not correspond to any configured version stream. Based on lock file evidence:

- Affected versions in scoped stream (2.2.x): RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- Not affected (fixed): RHTPA 2.2.3, RHTPA 2.2.4
- Cross-stream affected (2.1.x): RHTPA 2.1.0, RHTPA 2.1.1

The Affects Versions field should be corrected to include only the affected versions in the scoped stream: **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2** (removing RHTPA 2.0.0).
