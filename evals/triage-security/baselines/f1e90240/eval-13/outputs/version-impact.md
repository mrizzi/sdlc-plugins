# Step 2 -- Version Impact Analysis for CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build | Backend Tag | quinn-proto | Affected? | Notes |
|---------|--------|-------|-------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.3.8 | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.3.12 | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.4.5 | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.4.8 | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | 0.4.9 | v0.4.8 | 0.11.12 | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.4.11 | v0.4.11 | 0.11.14 | NO | fixed at 0.11.14 |
| 2.2.4 | 2.2.x | 0.4.12 | v0.4.12 | 0.11.14 | NO | fixed at 0.11.14 |

## Stream-Scoped Impact (this issue: 2.2.x)

Since TC-8001 is scoped to stream 2.2.x (suffix `[rhtpa-2.2]`), the directly relevant versions are:

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | 0.11.12 | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | fixed at 0.11.14 |
| 2.2.4 | 0.11.14 | NO | fixed at 0.11.14 |

**Result**: 3 versions affected (2.2.0, 2.2.1, 2.2.2), 2 versions not affected (2.2.3, 2.2.4).

## Cross-Stream Impact (Case B)

Stream 2.1.x is **also affected** (both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9):

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.1.0 | 0.11.9 | YES |
| 2.1.1 | 0.11.9 | YES |

This cross-stream impact triggers Case B processing in Step 8 -- a cross-stream impact comment and potential preemptive remediation task creation for 2.1.x.

## Affects Versions Correction (Step 3 Input)

- **Current** (PSIRT-assigned): `[RHTPA 2.0.0]`
- **Proposed** (scoped to 2.2.x): `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

RHTPA 2.0.0 does not correspond to any configured version stream. The correct Affects Versions for this stream-scoped issue are the 2.2.x versions that are actually affected per lock file analysis. Versions 2.2.3 and 2.2.4 are NOT affected (they already ship the fix at 0.11.14) and must not be included.

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD (from matrix latest tag) | Fixed? |
|--------|-----------|-----------------|------------------------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (latest tag v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (latest tag v0.4.12) | YES |

- Stream 2.2.x: The upstream branch `release/0.4.z` already has the fix (v0.4.11+ ships 0.11.14). Remediation for 2.2.x is a Konflux release repo change: bump the source tag to a version that includes the fix.
- Stream 2.1.x: The upstream branch `release/0.3.z` does NOT have the fix (latest is still 0.11.9). Remediation for 2.1.x requires an upstream PR first.
