# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8, quinn-proto 0.11.12) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Summary

- **Affected versions in scoped stream (2.2.x):** 2.2.0, 2.2.1, 2.2.2
- **Not affected in scoped stream (2.2.x):** 2.2.3, 2.2.4
- **Cross-stream impact (2.1.x):** 2.1.0 and 2.1.1 are also affected (quinn-proto 0.11.9 < 0.11.14)

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD (v0.4.12) | Fixed? |
|--------|-----------|-----------------|---------------------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 | NO |

The 2.2.x stream has the fix available upstream at tag v0.4.11+. Remediation for affected 2.2.x versions involves bumping the backend source reference to v0.4.11 or later.

The 2.1.x stream does NOT have the fix upstream (release/0.3.z still ships 0.11.9). Remediation would require backporting the quinn-proto bump to the release/0.3.z branch first.
