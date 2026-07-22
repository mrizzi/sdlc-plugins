# Version Impact Analysis — CVE-2026-28940

## Step 2.1 — Supportability Matrix

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## Step 2.3 — Dependency Version Extraction

serde_json versions extracted from `Cargo.lock` at each pinned backend tag:

| Tag | serde_json version | Source |
|-----|--------------------|--------|
| `v0.3.8` | 1.0.137 | `git show v0.3.8:Cargo.lock` |
| `v0.3.12` | 1.0.137 | `git show v0.3.12:Cargo.lock` |
| `v0.4.5` | 1.0.138 | `git show v0.4.5:Cargo.lock` |
| `v0.4.8` | 1.0.138 | `git show v0.4.8:Cargo.lock` |
| `v0.4.9` | _(retag of v0.4.8)_ | same as v0.4.8 |
| `v0.4.11` | 1.0.139 | `git show v0.4.11:Cargo.lock` |
| `v0.4.12` | 1.0.139 | `git show v0.4.12:Cargo.lock` |

## Step 2.4 — Version Impact Table

CVE-2026-28940 affects serde_json versions **before 1.0.135**. Fixed version: **1.0.135**.

### Scoped stream (2.2.x) — issue stream

| Version | serde_json | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.2.0 | 1.0.138 | **NO** | >= 1.0.135 (fixed) |
| 2.2.1 | 1.0.138 | **NO** | >= 1.0.135 (fixed) |
| 2.2.2 | -- | **NO** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 1.0.139 | **NO** | >= 1.0.135 (fixed) |
| 2.2.4 | 1.0.139 | **NO** | >= 1.0.135 (fixed) |

### Other stream (2.1.x) — cross-stream check

| Version | serde_json | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.1.0 | 1.0.137 | **NO** | >= 1.0.135 (fixed) |
| 2.1.1 | 1.0.137 | **NO** | >= 1.0.135 (fixed) |

## Summary

**No supported versions are affected.** Every version across all streams ships serde_json >= 1.0.135, which is at or above the fix threshold. The vulnerability (serde_json < 1.0.135) does not apply to any shipped product version.

- Stream 2.2.x: all 5 versions ship serde_json 1.0.138 or 1.0.139 — NOT affected
- Stream 2.1.x: all 2 versions ship serde_json 1.0.137 — NOT affected
