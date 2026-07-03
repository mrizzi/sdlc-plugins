# Version Impact Analysis -- CVE-2026-28940

## Fix Threshold

- Vulnerable library: **serde_json**
- Affected range: versions **before 1.0.135** (< 1.0.135)
- Fixed version: **1.0.135**

## Dependency Version Extraction

Dependency versions extracted from lock file data (simulated `git show <tag>:Cargo.lock` output):

### Stream 2.1.x (rhtpa-release.0.3.z)

| Tag | serde_json version |
|-----|--------------------|
| v0.3.8 | 1.0.137 |
| v0.3.12 | 1.0.137 |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Tag | serde_json version |
|-----|--------------------|
| v0.4.5 | 1.0.138 |
| v0.4.8 | 1.0.138 |
| v0.4.9 | _(retag of v0.4.8)_ |
| v0.4.11 | 1.0.139 |
| v0.4.12 | 1.0.139 |

## Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Version | Stream | Build Tag | serde_json | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 1.0.137 | **NO** | >= 1.0.135 |
| 2.1.1 | 2.1.x | v0.3.12 | 1.0.137 | **NO** | >= 1.0.135 |
| 2.2.0 | 2.2.x | v0.4.5 | 1.0.138 | **NO** | >= 1.0.135 |
| 2.2.1 | 2.2.x | v0.4.8 | 1.0.138 | **NO** | >= 1.0.135 |
| 2.2.2 | 2.2.x | v0.4.9 | 1.0.138 | **NO** | retag of 2.2.1, same as v0.4.8 |
| 2.2.3 | 2.2.x | v0.4.11 | 1.0.139 | **NO** | >= 1.0.135 |
| 2.2.4 | 2.2.x | v0.4.12 | 1.0.139 | **NO** | >= 1.0.135 |

## Summary

**No supported versions are affected.** Every version across both the 2.1.x and 2.2.x streams ships serde_json >= 1.0.137, which is well above the fix threshold of 1.0.135. The vulnerability (stack overflow on deeply nested JSON input) was fixed in serde_json 1.0.135 and all shipped versions include that fix.

- Minimum shipped version: **1.0.137** (stream 2.1.x)
- Maximum shipped version: **1.0.139** (stream 2.2.x, versions 2.2.3 and 2.2.4)
- Fix threshold: **1.0.135**
- All shipped versions exceed the fix threshold by at least 2 patch versions.
