# Version Impact Analysis: TC-8002 (CVE-2026-28940)

## Vulnerability Threshold

- **Affected package**: serde_json
- **Vulnerable versions**: < 1.0.135
- **Fixed version**: >= 1.0.135

## Stream 1: 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Backend Tag | serde_json Version | Vulnerable? |
|---------|-------|-------------|-------------------|-------------|
| 2.1.0 | 0.3.8 | v0.3.8 | 1.0.137 | No (>= 1.0.135) |
| 2.1.1 | 0.3.12 | v0.3.12 | 1.0.137 | No (>= 1.0.135) |

**Stream 2.1.x result**: NOT AFFECTED -- all shipped versions include serde_json >= 1.0.137, which is above the fix threshold of 1.0.135.

## Stream 2: 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Backend Tag | serde_json Version | Vulnerable? |
|---------|-------|-------------|-------------------|-------------|
| 2.2.0 | 0.4.5 | v0.4.5 | 1.0.138 | No (>= 1.0.135) |
| 2.2.1 | 0.4.8 | v0.4.8 | 1.0.138 | No (>= 1.0.135) |
| 2.2.2 | 0.4.9 | v0.4.8 | 1.0.138 (retag of v0.4.8) | No (>= 1.0.135) |
| 2.2.3 | 0.4.11 | v0.4.11 | 1.0.139 | No (>= 1.0.135) |
| 2.2.4 | 0.4.12 | v0.4.12 | 1.0.139 | No (>= 1.0.135) |

**Stream 2.2.x result**: NOT AFFECTED -- all shipped versions include serde_json >= 1.0.138, which is above the fix threshold of 1.0.135.

## Summary

| Stream | Earliest serde_json | Fix Threshold | Status |
|--------|---------------------|---------------|--------|
| 2.1.x | 1.0.137 | 1.0.135 | Not affected |
| 2.2.x | 1.0.138 | 1.0.135 | Not affected |

**Overall finding**: CVE-2026-28940 does NOT affect any shipped version across any supported stream. Every build in both the 2.1.x and 2.2.x streams ships serde_json at version 1.0.137 or higher, which already includes the fix (1.0.135). The vulnerability was fixed upstream before the earliest build in either stream was produced.
