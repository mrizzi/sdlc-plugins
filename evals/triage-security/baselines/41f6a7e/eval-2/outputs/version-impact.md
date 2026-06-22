# Version Impact Analysis: TC-8002 (CVE-2026-28940)

## Vulnerability Threshold

- **Affected package**: serde_json
- **Vulnerable versions**: < 1.0.135
- **Fixed version**: >= 1.0.135

## Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | serde_json Version | Vulnerable? |
|---------|-----------|-------------------|-------------|
| 2.1.0 | v0.3.8 | 1.0.137 | No (>= 1.0.135) |
| 2.1.1 | v0.3.12 | 1.0.137 | No (>= 1.0.135) |

**Stream result**: Not affected. All versions ship serde_json 1.0.137, which is above the fix threshold of 1.0.135.

## Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build Tag | serde_json Version | Vulnerable? |
|---------|-----------|-------------------|-------------|
| 2.2.0 | v0.4.5 | 1.0.138 | No (>= 1.0.135) |
| 2.2.1 | v0.4.8 | 1.0.138 | No (>= 1.0.135) |
| 2.2.2 | v0.4.9 | 1.0.138 (retag of v0.4.8) | No (>= 1.0.135) |
| 2.2.3 | v0.4.11 | 1.0.139 | No (>= 1.0.135) |
| 2.2.4 | v0.4.12 | 1.0.139 | No (>= 1.0.135) |

**Stream result**: Not affected. All versions ship serde_json >= 1.0.138, which is above the fix threshold of 1.0.135.

## Summary

| Stream | Versions Checked | Affected Count | Status |
|--------|-----------------|----------------|--------|
| 2.1.x | 2 | 0 | Not Affected |
| 2.2.x | 5 | 0 | Not Affected |
| **Total** | **7** | **0** | **Not Affected** |

No shipped version across any supported stream contains a vulnerable version of serde_json. The earliest shipped version (2.1.0, tag v0.3.8) already includes serde_json 1.0.137, which is two patch versions above the fix (1.0.135). The vulnerability was fixed upstream before any RHTPA release shipped.
