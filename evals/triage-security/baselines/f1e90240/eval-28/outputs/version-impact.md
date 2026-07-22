# Step 2 — Version Impact Analysis: CVE-2026-99010 (h2)

## 2.2.x Stream — Version Impact Table

Version Impact for CVE-2026-99010 (h2 < 0.4.5):

| Version | Backend Tag | h2 version | Affected? | Notes |
|---------|-------------|------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 0.4.4 | YES | |
| 2.2.1 | `v0.4.8` | 0.4.4 | YES | |
| 2.2.2 | `v0.4.9` | — | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 0.4.5 | NO | ships fixed version |
| 2.2.4 | `v0.4.12` | 0.4.5 | NO | ships fixed version |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 ship h2 0.4.4 which is within the affected range (< 0.4.5). Versions 2.2.3 and 2.2.4 ship h2 0.4.5 (the fix version) and are NOT affected.

## Cross-Stream Check (2.1.x)

| Version | Backend Tag | h2 version | Affected? | Notes |
|---------|-------------|------------|-----------|-------|
| 2.1.0 | `v0.3.8` | 0.4.5 | NO | ships fixed version |
| 2.1.1 | `v0.3.12` | 0.4.5 | NO | ships fixed version |

The 2.1.x stream is NOT affected. No cross-stream impact notice (Case B) is needed.

## Step 2.3.5 — Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> reqwest -> hyper -> h2
  Type: transitive (3 levels deep)
  Profile: production (reqwest is a runtime dependency)

First appeared: 2.1.0 (initial project setup -- reqwest has always depended on hyper/h2)
Present in all versions
```

**Manifest evidence:**

h2 is NOT a direct dependency of the backend workspace. It enters the dependency tree transitively:

```toml
# backend/Cargo.toml (all versions)
[dependencies]
reqwest = { version = "0.12", features = ["json"] }
# h2 is NOT a direct dependency -- it comes through reqwest -> hyper -> h2
```

**Dependency path**: `backend` -> `reqwest 0.12.5` -> `hyper 1.4.1` -> `h2 0.4.4`

**Remediation complexity**: This is a transitive dependency 3 levels deep. The remediation approach is two-tier:

1. **Preferred**: Bump `reqwest` (the direct dependency) to a version whose transitive closure includes h2 >= 0.4.5. This avoids adding h2 as a direct dependency.
2. **Fallback**: If no reqwest version resolves h2 >= 0.4.5 (or if bumping reqwest introduces breaking API changes), pin h2 directly via `cargo add h2@0.4.5` to override the transitive resolution.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.2.x | Cargo | `release/0.4.z` | Fix available upstream (h2 0.4.5 released, PR hyperium/h2#800 merged) |

The upstream fix is available. Remediation is a source repo change to bump the dependency, followed by a Konflux release repo update to pick up the new source commit.
