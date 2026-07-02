# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix

Loaded from security-matrix-mock.md (Last-Updated: 2026-06-28T10:00:00Z).

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 | |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 | |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | |

## 2.3 -- Dependency Version Extraction

Ecosystem: Cargo
Lock file: Cargo.lock
Library: serde_json
Fix threshold: 1.0.135 (versions before 1.0.135 are vulnerable)

Extracted serde_json versions from lock file data at each pinned commit:

| Tag | serde_json version | Comparison to fix threshold (1.0.135) |
|-----|--------------------|---------------------------------------|
| v0.3.8 | 1.0.137 | 1.0.137 >= 1.0.135 -- NOT vulnerable |
| v0.3.12 | 1.0.137 | 1.0.137 >= 1.0.135 -- NOT vulnerable |
| v0.4.5 | 1.0.138 | 1.0.138 >= 1.0.135 -- NOT vulnerable |
| v0.4.8 | 1.0.138 | 1.0.138 >= 1.0.135 -- NOT vulnerable |
| v0.4.9 | _(retag of v0.4.8)_ | same as v0.4.8 -- NOT vulnerable |
| v0.4.11 | 1.0.139 | 1.0.139 >= 1.0.135 -- NOT vulnerable |
| v0.4.12 | 1.0.139 | 1.0.139 >= 1.0.135 -- NOT vulnerable |

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Version | Stream | serde_json | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 1.0.137 | NO | ships patched version |
| 2.1.1 | 2.1.x | 1.0.137 | NO | ships patched version |
| 2.2.0 | 2.2.x | 1.0.138 | NO | ships patched version |
| 2.2.1 | 2.2.x | 1.0.138 | NO | ships patched version |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 1.0.139 | NO | ships patched version |
| 2.2.4 | 2.2.x | 1.0.139 | NO | ships patched version |

**Result: NO supported versions are affected.** All versions across both streams ship
serde_json >= 1.0.135, which is at or above the fix threshold. The vulnerability
(stack overflow on deeply nested input, fixed in 1.0.135) does not apply to any
shipped version.

### Dependency chain context

Not applicable -- no versions are affected. All shipped serde_json versions (1.0.137,
1.0.138, 1.0.139) already include the recursion limit fix introduced in 1.0.135.

## 2.5 -- Upstream Fix Check

Not applicable -- since no supported versions are affected, upstream fix status
is moot. For completeness:

| Stream | Ecosystem | Upstream Branch | Latest shipped version | Fixed? |
|--------|-----------|-----------------|------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 1.0.137 | YES (already shipping fixed version) |
| 2.2.x | Cargo | release/0.4.z | 1.0.139 | YES (already shipping fixed version) |
