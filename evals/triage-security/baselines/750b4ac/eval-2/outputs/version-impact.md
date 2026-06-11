# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-28940 (serde_json < 1.0.135)

Per Important Rule 4, all supported versions across all streams are checked -- not just the 2.2.x stream scoped in the issue summary.

| Version | Stream | Tag | serde_json | Affected? | Notes |
|---------|--------|-----|------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 1.0.137 | NO | 1.0.137 >= 1.0.135 |
| 2.1.1 | 2.1.x | v0.3.12 | 1.0.137 | NO | 1.0.137 >= 1.0.135 |
| 2.2.0 | 2.2.x | v0.4.5 | 1.0.138 | NO | 1.0.138 >= 1.0.135 |
| 2.2.1 | 2.2.x | v0.4.8 | 1.0.138 | NO | 1.0.138 >= 1.0.135 |
| 2.2.2 | 2.2.x | v0.4.9 | -- | NO | retag of v0.4.8 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 1.0.139 | NO | 1.0.139 >= 1.0.135 |
| 2.2.4 | 2.2.x | v0.4.12 | 1.0.139 | NO | 1.0.139 >= 1.0.135 |

## Analysis Summary

**No supported versions are affected.** Every version across both streams ships serde_json >= 1.0.137, which is outside the affected range (< 1.0.135). The fix (1.0.135) was already present in serde_json before any of these product versions were built.

- Earliest serde_json version shipped: **1.0.137** (in v0.3.8, built 2025-09-15)
- CVE fix version: **1.0.135**
- All shipped versions exceed the fix threshold by at least 2 patch versions.

## Dependency Chain Context

Since no versions are affected, dependency chain tracing (Step 2.3.5) is not required. The vulnerable version of serde_json (< 1.0.135) was never shipped in any supported product version.

## Upstream Fix Check

Not applicable -- no versions are affected, so no remediation path is needed. The upstream fix (serde_json 1.0.135) was already incorporated before the earliest supported version was built.
