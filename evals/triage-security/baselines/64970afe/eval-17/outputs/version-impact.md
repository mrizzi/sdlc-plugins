# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Supportability Matrix (Aggregated)

Data loaded from security-matrix.md files for both version streams.
Matrix Last-Updated: 2026-06-28T10:00:00Z (11 days ago -- within 14-day freshness threshold).

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend tag | quinn-proto version |
|---------|-------|------------|-------------|---------------------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 | 0.11.9 |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 | 0.11.9 |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend tag | quinn-proto version |
|---------|-------|------------|-------------|---------------------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | 0.11.9 |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | 0.11.12 |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | -- (retag of 2.2.1) |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | 0.11.14 |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | 0.11.14 |

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

## Fix Threshold

- Jira description: fixed version 0.11.14 (affected range: < 0.11.14)
- Fix threshold used for comparison: **0.11.14**

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (present in Cargo.lock at workspace level)
  Profile: production (quinn-proto is a runtime dependency for QUIC transport)
  Ecosystem: Cargo

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

quinn-proto is a direct dependency of the backend workspace. This is a
straightforward version bump -- no transitive dependency chain complications.

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | (to be checked) | TBD |
| 2.2.x | Cargo | release/0.4.z | (to be checked) | TBD |

Based on the supportability matrix, the fix (quinn-proto 0.11.14) first
appeared at tag v0.4.11 (stream 2.2.x, version 2.2.3). Versions 2.2.3 and
2.2.4 already ship the fixed version. The 2.1.x stream has not yet picked
up the fix (latest tag v0.3.12 still ships quinn-proto 0.11.9).

## Cross-Stream Impact Summary

- **Issue stream scope**: 2.2.x (from suffix `[rhtpa-2.2]`)
- **Affected within scope (2.2.x)**: 2.2.0, 2.2.1, 2.2.2
- **Not affected within scope (2.2.x)**: 2.2.3, 2.2.4 (ship fixed version)
- **Affected outside scope (2.1.x)**: 2.1.0, 2.1.1 -- cross-stream impact detected
