# Version Impact Analysis — CVE-2026-28940 (serde_json < 1.0.135)

## Step 2.3 — Dependency Version Extraction

Extracted serde_json versions from `Cargo.lock` at each pinned source commit:

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Backend Tag | serde_json version | Source |
|---------|-------|-------------|--------------------|--------|
| 2.1.0 | 0.3.8 | `v0.3.8` | 1.0.137 | `git show v0.3.8:Cargo.lock` |
| 2.1.1 | 0.3.12 | `v0.3.12` | 1.0.137 | `git show v0.3.12:Cargo.lock` |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Backend Tag | serde_json version | Source |
|---------|-------|-------------|--------------------|--------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 1.0.138 | `git show v0.4.5:Cargo.lock` |
| 2.2.1 | 0.4.8 | `v0.4.8` | 1.0.138 | `git show v0.4.8:Cargo.lock` |
| 2.2.2 | 0.4.9 | `v0.4.8` | 1.0.138 | retag of 2.2.1 (same source) |
| 2.2.3 | 0.4.11 | `v0.4.11` | 1.0.139 | `git show v0.4.11:Cargo.lock` |
| 2.2.4 | 0.4.12 | `v0.4.12` | 1.0.139 | `git show v0.4.12:Cargo.lock` |

## Step 2.4 — Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Version | Stream | serde_json | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 1.0.137 | NO | >= 1.0.135 (fixed) |
| 2.1.1 | 2.1.x | 1.0.137 | NO | >= 1.0.135 (fixed) |
| 2.2.0 | 2.2.x | 1.0.138 | NO | >= 1.0.135 (fixed) |
| 2.2.1 | 2.2.x | 1.0.138 | NO | >= 1.0.135 (fixed) |
| 2.2.2 | 2.2.x | 1.0.138 | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 1.0.139 | NO | >= 1.0.135 (fixed) |
| 2.2.4 | 2.2.x | 1.0.139 | NO | >= 1.0.135 (fixed) |

**Result: NO supported versions are affected.**

All supported versions across both streams ship serde_json >= 1.0.135, which is at or above the fix threshold. The vulnerable range (< 1.0.135) is not present in any shipped version.

- Stream 2.1.x: all versions ship serde_json 1.0.137 (fixed)
- Stream 2.2.x: all versions ship serde_json 1.0.138 or 1.0.139 (fixed)

## Step 2.5 — Upstream Fix Status

Not applicable. No versions are affected, so upstream fix status is moot. For completeness:

| Stream | Ecosystem | Upstream Branch | serde_json at latest tag | Fixed? |
|--------|-----------|-----------------|--------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 1.0.137 (at v0.3.12) | YES |
| 2.2.x | Cargo | release/0.4.z | 1.0.139 (at v0.4.12) | YES |

All upstream branches already carry the fix.
