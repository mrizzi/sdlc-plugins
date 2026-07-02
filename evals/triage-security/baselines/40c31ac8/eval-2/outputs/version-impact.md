# Version Impact Analysis -- CVE-2026-28940

## serde_json -- affected versions: before 1.0.135, fixed in 1.0.135

### Version Impact Table

All streams are analyzed to determine cross-stream impact, even though TC-8002 is scoped to the 2.2.x stream.

| Stream | Version | Build Tag | serde_json version | Affected? | Notes |
|--------|---------|-----------|-------------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 1.0.137 | NO | >= 1.0.135 |
| 2.1.x | 2.1.1 | v0.3.12 | 1.0.137 | NO | >= 1.0.135 |
| 2.2.x | 2.2.0 | v0.4.5 | 1.0.138 | NO | >= 1.0.135 |
| 2.2.x | 2.2.1 | v0.4.8 | 1.0.138 | NO | >= 1.0.135 |
| 2.2.x | 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 1.0.139 | NO | >= 1.0.135 |
| 2.2.x | 2.2.4 | v0.4.12 | 1.0.139 | NO | >= 1.0.135 |

### Summary

**No supported versions are affected.** Every version across both streams (2.1.x and 2.2.x) ships serde_json >= 1.0.135, which is at or above the fix threshold. The earliest shipped version (1.0.137 in 2.1.0) already exceeds the fix version (1.0.135).

### Dependency Chain Context

Not applicable -- since no versions are affected, dependency chain tracing for remediation purposes is not needed. For reference, serde_json is a direct Cargo dependency of the backend workspace, used for JSON serialization/deserialization.

### Upstream Fix Status

Not applicable -- all shipped versions already include the fix. No upstream backport is required.
