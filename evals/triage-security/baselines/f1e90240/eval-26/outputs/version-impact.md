# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-99001 (criterion < 0.5.2)

### Scoped stream: 2.2.x

| Version | Build | Backend Tag | criterion version | Affected? | Notes |
|---------|-------|-------------|-------------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 0.5.1 | YES | |
| 2.2.1 | 0.4.8 | `v0.4.8` | 0.5.1 | YES | |
| 2.2.2 | 0.4.9 | `v0.4.8` | 0.5.1 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.11 | `v0.4.11` | 0.5.1 | YES | |
| 2.2.4 | 0.4.12 | `v0.4.12` | 0.5.1 | YES | |

All 2.2.x versions ship criterion 0.5.1, which is within the affected range
(versions before 0.5.2). All versions are affected.

### Cross-stream analysis (2.1.x -- outside issue scope)

| Version | Build | Backend Tag | criterion version | Affected? | Notes |
|---------|-------|-------------|-------------------|-----------|-------|
| 2.1.0 | 0.3.8 | `v0.3.8` | 0.5.1 | YES | |
| 2.1.1 | 0.3.12 | `v0.3.12` | 0.5.1 | YES | |

The 2.1.x stream is also affected (criterion 0.5.1 < 0.5.2 fix threshold).
This cross-stream impact is noted for Case B handling in Step 8.

## Step 2.3.5 -- Dependency Chain Context

```
Dependency chain for criterion:
  backend (workspace) -> criterion (direct dev-dependency)
  Type: direct dependency
  Profile: dev-only ([dev-dependencies] in backend/Cargo.toml)
  NOT present in production builds -- used for benchmarks only

First appeared: 2.1.0 (initial project setup)
Present in all versions
```

Manifest evidence:
```toml
# backend/Cargo.toml (all versions)
[dev-dependencies]
criterion = "0.5.1"
```

### Dependency Scope Assessment

criterion is declared in `[dev-dependencies]` in `backend/Cargo.toml`. Dev-only
dependencies are NOT shipped in production builds -- they are used for benchmarks
and tests only.

Per the dependency scope decision tree:
- criterion is a **dev-only dependency** and is not shipped in production
- Still create remediation tasks (supply chain risk), but with modifications:
  - Add the `dev-dependency` label to the remediation task
  - Set priority to **Normal** regardless of CVE severity (CVSS 5.3 Medium)
  - Include a note: "This dependency is dev/build-only and is not shipped in
    production. Remediation priority is Normal (supply chain risk only)."

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Lock File | Notes |
|--------|-----------|-----------------|-----------|-------|
| 2.2.x | Cargo | release/0.4.z | Cargo.lock | Upstream fix status would be checked via `git show release/0.4.z:Cargo.lock` |
