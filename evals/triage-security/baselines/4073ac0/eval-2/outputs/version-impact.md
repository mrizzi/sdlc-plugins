# Step 2 -- Version Impact Analysis

## CVE Details

- **CVE**: CVE-2026-28940
- **Library**: serde_json
- **Affected range**: versions before 1.0.135
- **Fixed version**: 1.0.135

## Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Version | Stream | Tag | serde_json | Affected? | Notes |
|---------|--------|-----|------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 1.0.137 | NO | Ships patched version (>= 1.0.135) |
| 2.1.1 | 2.1.x | `v0.3.12` | 1.0.137 | NO | Ships patched version (>= 1.0.135) |
| 2.2.0 | 2.2.x | `v0.4.5` | 1.0.138 | NO | Ships patched version (>= 1.0.135) |
| 2.2.1 | 2.2.x | `v0.4.8` | 1.0.138 | NO | Ships patched version (>= 1.0.135) |
| 2.2.2 | 2.2.x | `v0.4.9` | 1.0.138 | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 1.0.139 | NO | Ships patched version (>= 1.0.135) |
| 2.2.4 | 2.2.x | `v0.4.12` | 1.0.139 | NO | Ships patched version (>= 1.0.135) |

**Result: NO supported versions are affected.** Every version across all streams ships serde_json >= 1.0.135, which is at or above the fixed version. The vulnerable version range (< 1.0.135) was never shipped in any supported product release.

## Evidence Summary

- **Stream 2.1.x**: All versions ship serde_json 1.0.137 (2 versions above the fix)
- **Stream 2.2.x**: All versions ship serde_json 1.0.138 or 1.0.139 (3-4 versions above the fix)
- The lowest serde_json version found across all streams is **1.0.137** (in 2.1.0 and 2.1.1), which is still above the fixed version 1.0.135
- Version 2.2.2 is a retag of 2.2.1 (backend `v0.4.9` is a retag of `v0.4.8`), so the serde_json version is carried forward as 1.0.138

## Dependency Chain Context

Not applicable -- since no versions are affected (all ship a version of serde_json outside the vulnerable range), dependency chain tracing for remediation context is not needed.

## Upstream Fix Status

Not applicable -- since no supported versions are affected, upstream fix status is moot. The fix (serde_json 1.0.135) was already incorporated into the dependency tree before the earliest supported version was built.
