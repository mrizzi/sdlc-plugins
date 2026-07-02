# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Stream Impact Summary

| Stream | Affected Versions | Unaffected Versions | Status |
|--------|-------------------|---------------------|--------|
| 2.1.x | 2.1.0, 2.1.1 | (none) | All versions affected |
| 2.2.x | 2.2.0, 2.2.1, 2.2.2 | 2.2.3, 2.2.4 | Fix present in 2.2.3+ |

## Issue Scope

The issue is scoped to stream **2.2.x** (from summary suffix `[rhtpa-2.2]`).

- **In-scope stream (2.2.x):** Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14 (the fixed version).
- **Cross-stream impact (2.1.x):** All versions (2.1.0, 2.1.1) are affected. This stream is outside the issue's scope and is handled as Case B (proactive/preemptive remediation).

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Build Tag Version | Fixed at Latest? |
|--------|-----------|-----------------|--------------------------|------------------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.12) | YES |

- **Stream 2.2.x:** The upstream branch `release/0.4.z` already contains the fix (quinn-proto 0.11.14 at latest tags v0.4.11, v0.4.12). Remediation for this stream is a downstream propagation to ensure the Affects Versions are corrected.
- **Stream 2.1.x:** The upstream branch `release/0.3.z` does NOT contain the fix (quinn-proto 0.11.9 at latest tag v0.3.12). Remediation for this stream requires an upstream backport first, then downstream propagation.

## Affects Versions Correction

The PSIRT-assigned Affects Versions of **RHTPA 2.0.0** is incorrect -- no 2.0.x stream exists. Based on the version impact analysis, the corrected Affects Versions should be:

- **RHTPA 2.1.0** (quinn-proto 0.11.9 -- affected)
- **RHTPA 2.1.1** (quinn-proto 0.11.9 -- affected)
- **RHTPA 2.2.0** (quinn-proto 0.11.9 -- affected)
- **RHTPA 2.2.1** (quinn-proto 0.11.12 -- affected)
- **RHTPA 2.2.2** (retag of 2.2.1 -- affected)

Remove: RHTPA 2.0.0 (no such stream exists).
