# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-99010 (h2 < 0.4.5)

### Scoped stream: 2.2.x

| Version | Build | Backend Tag | h2 version | Affected? | Notes |
|---------|-------|-------------|------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 0.4.4 | YES | |
| 2.2.1 | 0.4.8 | `v0.4.8` | 0.4.4 | YES | |
| 2.2.2 | 0.4.9 | `v0.4.8` | 0.4.4 | YES | retag of 2.2.1 |
| 2.2.3 | 0.4.11 | `v0.4.11` | 0.4.5 | NO | fixed at 0.4.5 |
| 2.2.4 | 0.4.12 | `v0.4.12` | 0.4.5 | NO | fixed at 0.4.5 |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 ship h2 0.4.4, which is within the affected range (< 0.4.5). Versions 2.2.3 and 2.2.4 ship h2 0.4.5, which is at or above the fix threshold.

### Cross-stream check: 2.1.x

| Version | Build | Backend Tag | h2 version | Affected? | Notes |
|---------|-------|-------------|------------|-----------|-------|
| 2.1.0 | 0.3.8 | `v0.3.8` | 0.4.5 | NO | at fix threshold |
| 2.1.1 | 0.3.12 | `v0.3.12` | 0.4.5 | NO | at fix threshold |

**Cross-stream result**: The 2.1.x stream is NOT affected. All versions ship h2 0.4.5 which is at the fix threshold.

## Step 2.3.5 -- Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> reqwest -> hyper -> h2
  Type: transitive (3 levels deep)
  Profile: production (reqwest is a runtime dependency)

First appeared: 2.1.0 (initial project setup -- reqwest has always depended on hyper/h2)
Present in all versions
```

**Manifest evidence:**
```toml
# backend/Cargo.toml (all versions)
[dependencies]
reqwest = { version = "0.12", features = ["json"] }
# h2 is NOT a direct dependency -- it comes through reqwest -> hyper -> h2
```

**Lock file evidence (affected versions 2.2.0-2.2.2):**
```
[[package]]
name = "h2"
version = "0.4.4"

[[package]]
name = "hyper"
version = "1.4.1"
dependencies = ["h2"]

[[package]]
name = "reqwest"
version = "0.12.5"
dependencies = ["hyper"]
```

**Lock file evidence (fixed versions 2.2.3+):**
```
[[package]]
name = "h2"
version = "0.4.5"
```

### Remediation Context

h2 is a **transitive** dependency (3 levels deep: reqwest -> hyper -> h2). This means:

- A direct version bump of h2 in `Cargo.toml` is not possible -- h2 is not listed as a direct dependency.
- The two-tier remediation approach applies:
  1. **Preferred**: bump `reqwest` to a version whose transitive closure includes h2 >= 0.4.5
  2. **Fallback**: pin h2 directly via `cargo add h2@0.4.5` to override the transitive resolution
- Coordination with intermediate package maintainers (reqwest, hyper) may be required if they pin the vulnerable h2 version.

## Step 2.5 -- Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | FIXED -- versions 2.2.3+ already ship h2 0.4.5 |

The upstream branch `release/0.4.z` already contains the fix. Versions 2.2.3 and 2.2.4 (built from tags v0.4.11 and v0.4.12 on this branch) ship h2 0.4.5. The remediation for affected versions (2.2.0-2.2.2) requires updating the source reference in the Konflux release repo to a tag that includes the fix.
