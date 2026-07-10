# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-99002 (rustls < 0.23.5)

Scoped to stream **2.2.x** per issue suffix `[rhtpa-2.2]`.

| Version | Build Tag | rustls version | Affected? | Notes |
|---------|-----------|----------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 0.23.4 | YES | |
| 2.2.1 | `v0.4.8` | 0.23.4 | YES | |
| 2.2.2 | `v0.4.9` | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 0.23.4 | YES | |
| 2.2.4 | `v0.4.12` | 0.23.4 | YES | |

All versions in the 2.2.x stream ship rustls 0.23.4, which is within the
affected range (< 0.23.5).

## Cross-Stream Context (informational)

The 2.1.x stream is **not affected** -- rustls is not present in any 2.1.x
version (not a dependency in v0.3.8 or v0.3.12). rustls was first introduced
in 2.2.0 as an alternative TLS backend.

## Step 2.3.5 -- Dependency Chain Context

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
```

**Manifest evidence:**
```toml
# backend/Cargo.toml (v0.4.5+)
[dependencies]
rustls = { version = "0.23.4", optional = true }

[features]
default = ["tls-native"]
tls-native = ["dep:native-tls"]
tls-rustls = ["dep:rustls"]
```

The vulnerable dependency `rustls` is declared as `optional = true` and is
only included when the non-default feature `tls-rustls` is explicitly enabled.
The product ships with the `default` feature set, which includes `tls-native`
(backed by `native-tls`) but does **not** include `tls-rustls`. Therefore,
rustls is not compiled into the default production binary.

This triggers the **feature-gated optional dependency** path in the dependency
scope decision tree (Step 2.3.5). The user must be presented with a VEX
justification prompt before remediation tasks are created.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | To be checked at branch HEAD |

Upstream fix PR: https://github.com/rustls/rustls/pull/2100
