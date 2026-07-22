# Step 2 -- Version Impact Analysis: CVE-2026-99002

## Version Impact Table

Issue is scoped to the **2.2.x** stream (`[rhtpa-2.2]`).

### 2.2.x stream (rhtpa-release.0.4.z)

Version Impact for CVE-2026-99002 (rustls < 0.23.5):

| Version | Build | backend tag | rustls version | Affected? | Notes |
|---------|-------|-------------|----------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 0.23.4 | YES* | First version with rustls (optional dep) |
| 2.2.1 | 0.4.8 | `v0.4.8` | 0.23.4 | YES* | |
| 2.2.2 | 0.4.9 | `v0.4.8` | 0.23.4 | YES* | retag of 2.2.1 |
| 2.2.3 | 0.4.11 | `v0.4.11` | 0.23.4 | YES* | |
| 2.2.4 | 0.4.12 | `v0.4.12` | 0.23.4 | YES* | |

**\*Feature-gated**: rustls is an optional dependency behind the non-default `tls-rustls` feature flag. The product ships with `tls-native` (default feature) enabled. See dependency chain context below.

### Cross-stream check (2.1.x -- out of scope, informational)

| Version | Build | backend tag | rustls version | Affected? | Notes |
|---------|-------|-------------|----------------|-----------|-------|
| 2.1.0 | 0.3.8 | `v0.3.8` | _(not present)_ | NO | rustls not a dependency in 2.1.x |
| 2.1.1 | 0.3.12 | `v0.3.12` | _(not present)_ | NO | rustls not a dependency in 2.1.x |

Cross-stream impact: **None**. The 2.1.x stream does not include rustls at all (it was introduced in 2.2.0 as an alternative TLS backend). No Case B action needed.

## Step 2.3.5 -- Dependency Chain Context

```
Dependency chain for rustls:
  backend (workspace) -> rustls (direct optional dependency)
  Type: direct dependency (optional = true)
  Profile: feature-gated (behind non-default feature "tls-rustls")

  Feature declaration (backend/Cargo.toml):
    [features]
    default = ["tls-native"]
    tls-native = ["dep:native-tls"]
    tls-rustls = ["dep:rustls"]

  Default features do NOT include "tls-rustls" -- the product ships with
  the "tls-native" feature enabled by default.

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

### Dependency Scope Assessment

The vulnerable dependency `rustls` is declared with `optional = true` and is gated behind the `tls-rustls` feature flag. The default feature set is `["tls-native"]`, which does **not** include `tls-rustls`. This means:

1. **Default builds do not compile or link rustls** -- the `tls-rustls` feature must be explicitly enabled at build time.
2. **The shipped product uses `tls-native`** (native-tls) as the TLS backend by default.
3. **rustls appears in Cargo.lock** because it is declared as an optional dependency, but it is not included in the default binary unless the feature flag is activated.

Per the dependency scope decision tree in the skill, this is a **feature-gated optional dependency** that requires a VEX justification prompt before proceeding with remediation.
