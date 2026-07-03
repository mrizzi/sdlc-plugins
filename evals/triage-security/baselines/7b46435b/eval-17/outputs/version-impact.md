# Step 2 -- Version Impact Analysis

## Vulnerability Summary

| Parameter | Value |
|-----------|-------|
| CVE | CVE-2026-31812 |
| Library | quinn-proto |
| Affected range | < 0.11.14 |
| Fixed version | 0.11.14 |
| Ecosystem | Cargo |
| Lock file | Cargo.lock |

## Issue Stream Scope

This issue is scoped to the **2.2.x** stream (from summary suffix `[rhtpa-2.2]`).
All streams are analyzed for version impact, but Steps 3-4 actions are scoped to 2.2.x.
Cross-stream impact triggers Case B handling.

## Version Impact Table -- Stream 2.2.x (scoped)

| Version | Build | Tag | quinn-proto version | Affected? | Notes |
|---------|-------|-----|---------------------|-----------|-------|
| 2.2.0 | 0.4.5 | v0.4.5 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.2.1 | 0.4.8 | v0.4.8 | 0.11.12 | **YES** | 0.11.12 < 0.11.14 |
| 2.2.2 | 0.4.9 | v0.4.9 | 0.11.12 | **YES** | Retag of v0.4.8 -- same as 2.2.1 |
| 2.2.3 | 0.4.11 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | 0.4.12 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

**Stream 2.2.x finding**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. The fix was
incorporated starting with version 2.2.3 (build 0.4.11), which ships quinn-proto 0.11.14.
The latest version (2.2.4) also ships the fixed version.

Version 2.2.2 is a retag of 2.2.1 (tag v0.4.9 reuses the same backend source as v0.4.8),
so the lock file check is skipped and the affected status is carried forward from 2.2.1.

## Version Impact Table -- Stream 2.1.x (cross-stream)

| Version | Build | Tag | quinn-proto version | Affected? | Notes |
|---------|-------|-----|---------------------|-----------|-------|
| 2.1.0 | 0.3.8 | v0.3.8 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.1.1 | 0.3.12 | v0.3.12 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |

**Stream 2.1.x finding**: All versions in this stream are affected. Both 2.1.0 and 2.1.1
ship quinn-proto 0.11.9, which is below the fix threshold of 0.11.14. No fix has been
incorporated in this stream.

## Combined Impact Summary

| Stream | Affected Versions | Fixed Versions | Remediation Needed? |
|--------|-------------------|----------------|---------------------|
| 2.2.x (scoped) | 2.2.0, 2.2.1, 2.2.2 | 2.2.3, 2.2.4 | No -- already fixed in latest releases (2.2.3+) |
| 2.1.x (cross-stream) | 2.1.0, 2.1.1 | None | **Yes** -- all versions vulnerable |

## Affects Versions Correction (Step 3 preview)

The current Jira Affects Versions is **RHTPA 2.0.0**, which does not correspond to any
configured version stream. Based on the version impact analysis scoped to 2.2.x:

- **Remove**: RHTPA 2.0.0 (no 2.0.x stream exists)
- **Add**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 (affected versions in 2.2.x stream)

Note: RHTPA 2.1.0 and RHTPA 2.1.1 are also affected but are outside this issue's
stream scope. Cross-stream impact is handled via Case B (see remediation).

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | **Yes** -- v0.4.11+ ship the fix |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 | **No** -- latest tag v0.3.12 still ships 0.11.9 |
