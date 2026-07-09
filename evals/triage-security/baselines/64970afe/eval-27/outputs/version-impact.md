# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

Stream scoped to **2.2.x** per issue suffix `[rhtpa-2.2]`.

Source: `security-matrix.md` for rhtpa-release.0.4.z (Last-Updated: 2026-06-28T10:00:00Z -- 11 days ago, within 14-day freshness threshold).

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction

Ecosystem: Cargo. Lock file: `Cargo.lock`. Library: rustls. Fix threshold: 0.23.5.

| Version | Tag | rustls version | Affected? | Notes |
|---------|-----|----------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.23.4 | YES | 0.23.4 < 0.23.5 (fix threshold) |
| 2.2.1 | v0.4.8 | 0.23.4 | YES | 0.23.4 < 0.23.5 (fix threshold) |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.23.4 | YES | 0.23.4 < 0.23.5 (fix threshold) |
| 2.2.4 | v0.4.12 | 0.23.4 | YES | 0.23.4 < 0.23.5 (fix threshold) |

All 2.2.x versions ship rustls 0.23.4 in the lock file, which is below the fix threshold of 0.23.5.

**However**, rustls is an optional dependency gated behind the non-default `tls-rustls` feature flag. See dependency chain context below.

## 2.3.5 -- Dependency Chain Context

```
Dependency chain for rustls:
  backend (workspace) -> rustls (direct optional dependency)
  Type: direct dependency (optional = true)
  Profile: feature-gated (optional = true, behind non-default feature "tls-rustls")
  Default features do NOT include "tls-rustls" -- the product ships with
  the "tls-native" feature enabled by default

Feature declaration:
  [features]
  default = ["tls-native"]
  tls-native = ["dep:native-tls"]
  tls-rustls = ["dep:rustls"]

First appeared: 2.2.0 (added as alternative TLS backend)
Not present in: 2.1.x (only native-tls was available)

Manifest evidence:
  # backend/Cargo.toml (v0.4.5+)
  [dependencies]
  rustls = { version = "0.23.4", optional = true }
```

**Key finding**: rustls is declared as `optional = true` in Cargo.toml and is only included when the `tls-rustls` feature is explicitly enabled. The default feature set is `["tls-native"]`, which does NOT include `tls-rustls`. The product as shipped uses native-tls, not rustls. The vulnerable library is present in the Cargo.lock but is not compiled into the default build, and the vulnerable code is not in the execute path of the shipped product.

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-99002 (rustls < 0.23.5):

| Version | rustls | Affected? | Notes |
|---------|--------|-----------|-------|
| 2.2.0 | 0.23.4 | YES (*) | feature-gated behind non-default `tls-rustls` |
| 2.2.1 | 0.23.4 | YES (*) | feature-gated behind non-default `tls-rustls` |
| 2.2.2 | -- | YES (*) | retag of 2.2.1 |
| 2.2.3 | 0.23.4 | YES (*) | feature-gated behind non-default `tls-rustls` |
| 2.2.4 | 0.23.4 | YES (*) | feature-gated behind non-default `tls-rustls` |

(*) rustls is present in the lock file at a vulnerable version, BUT it is an optional dependency gated behind the non-default `tls-rustls` feature flag. The default build ships with `tls-native` and does not compile or include rustls. See feature-gate prompt for VEX justification options.

## Cross-Stream Check

The issue is scoped to stream 2.2.x. Checking the 2.1.x stream for cross-stream impact:

| Tag | rustls version |
|-----|----------------|
| v0.3.8 | (not present) |
| v0.3.12 | (not present) |

rustls is **not present** in the 2.1.x stream (it was first introduced in 2.2.0 as an alternative TLS backend). No cross-stream impact for the 2.1.x stream.
