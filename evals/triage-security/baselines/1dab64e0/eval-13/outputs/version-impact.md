# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | at or above fix threshold |
| 2.2.4 | 2.2.x | 0.11.14 | NO | at or above fix threshold |

## Stream-Scoped Summary

This issue is scoped to stream **2.2.x** (suffix `[rhtpa-2.2]`).

**In-scope (2.2.x) affected versions**: 2.2.0, 2.2.1, 2.2.2
**In-scope (2.2.x) unaffected versions**: 2.2.3, 2.2.4

**Cross-stream (2.1.x) affected versions**: 2.1.0, 2.1.1
Stream 2.1.x is outside this issue's scope but is also affected -- triggers Case B (cross-stream impact) in Step 8.

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: source dependency (Cargo)
  Ecosystem: Cargo
  Lock file: Cargo.lock
```

The dependency was present in all checked versions across both streams.

## Source Data

Data extracted from the mock lock file data in security-matrix-mock.md:

| Tag | quinn-proto version | Fix threshold (0.11.14) |
|-----|---------------------|-------------------------|
| v0.3.8 (2.1.0) | 0.11.9 | BELOW -- affected |
| v0.3.12 (2.1.1) | 0.11.9 | BELOW -- affected |
| v0.4.5 (2.2.0) | 0.11.9 | BELOW -- affected |
| v0.4.8 (2.2.1) | 0.11.12 | BELOW -- affected |
| v0.4.9 (2.2.2) | (retag of v0.4.8) | BELOW -- affected (same as 2.2.1) |
| v0.4.11 (2.2.3) | 0.11.14 | AT threshold -- not affected |
| v0.4.12 (2.2.4) | 0.11.14 | AT threshold -- not affected |

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | Fix status would be checked via `git show release/0.3.z:Cargo.lock` |
| 2.2.x | Cargo | release/0.4.z | Fixed -- versions 2.2.3+ already ship quinn-proto 0.11.14 |

The 2.2.x stream already has the fix in later releases (2.2.3, 2.2.4 ship quinn-proto 0.11.14). Remediation is needed only for versions 2.2.0, 2.2.1, and 2.2.2 which ship older quinn-proto versions.

## Affects Versions Correction (Step 3)

The issue currently has Affects Versions set to `RHTPA 2.0.0`, which does not correspond to any configured version stream. Based on lock file analysis, the correct Affects Versions for the scoped stream (2.2.x) are:

- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14, which is at or above the fix threshold.
