# Step 2 -- Version Impact Analysis: CVE-2026-99001 (criterion)

## 2.1 -- Supportability Matrix (2.2.x stream, in scope)

Loaded from: rhtpa-release.0.4.z security-matrix.md
Last-Updated: 2026-06-28T10:00:00Z (11 days ago -- within 14-day freshness threshold)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 -- Dependency Version Extraction

Fix threshold: criterion >= 0.5.2 (from Jira description; external CVE enrichment would cross-validate)

| Version | Tag | criterion version | Affected? | Notes |
|---------|-----|-------------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 0.5.1 | YES | 0.5.1 < 0.5.2 |
| 2.2.1 | `v0.4.8` | 0.5.1 | YES | 0.5.1 < 0.5.2 |
| 2.2.2 | `v0.4.9` | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 0.5.1 | YES | 0.5.1 < 0.5.2 |
| 2.2.4 | `v0.4.12` | 0.5.1 | YES | 0.5.1 < 0.5.2 |

**All 2.2.x versions are affected** -- all ship criterion 0.5.1, which is below the fix threshold of 0.5.2.

## Cross-stream Impact (2.1.x stream, out of scope)

Since this issue is scoped to 2.2.x, the 2.1.x stream is checked for cross-stream impact (Case B):

| Version | Tag | criterion version | Affected? | Notes |
|---------|-----|-------------------|-----------|-------|
| 2.1.0 | `v0.3.8` | 0.5.1 | YES | 0.5.1 < 0.5.2 |
| 2.1.1 | `v0.3.12` | 0.5.1 | YES | 0.5.1 < 0.5.2 |

The 2.1.x stream is also affected. Cross-stream impact applies (Case B).

## 2.3.5 -- Dependency Chain Context

```
Dependency chain for criterion:
  backend (workspace) -> criterion (direct dev-dependency)
  Type: direct dependency
  Profile: dev-only ([dev-dependencies] in backend/Cargo.toml)
  NOT present in production builds -- used for benchmarks only

First appeared: 2.1.0 (initial project setup)
Present in all versions
```

**Manifest evidence:**
```toml
# backend/Cargo.toml (all versions)
[dev-dependencies]
criterion = "0.5.1"
```

### Dependency Scope Assessment

criterion is declared in `[dev-dependencies]` and is NOT shipped in production builds. Per the dependency scope decision tree:

- **Classification**: Dev-only dependency (not shipped in production)
- **Risk**: Supply chain risk only -- compromised dev deps can inject malicious code during builds, but the vulnerable code (path traversal in benchmark output) does not affect production binaries or container images.
- **Remediation modifications**:
  - Add the `dev-dependency` label to all remediation tasks
  - Override priority to **Normal** regardless of CVE severity (Medium/5.3)
  - Include note: "This dependency is dev/build-only and is not shipped in production. Remediation priority is Normal (supply chain risk only)."

## 2.4 -- Version Impact Table (Summary)

Version Impact for CVE-2026-99001 (criterion < 0.5.2):

| Version | criterion | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.2.0 | 0.5.1 | YES | dev-dependency only |
| 2.2.1 | 0.5.1 | YES | dev-dependency only |
| 2.2.2 | -- | YES | retag of 2.2.1; dev-dependency only |
| 2.2.3 | 0.5.1 | YES | dev-dependency only |
| 2.2.4 | 0.5.1 | YES | dev-dependency only |

Cross-stream (2.1.x, out of scope):

| Version | criterion | Affected? | Notes |
|---------|-----------|-----------|-------|
| 2.1.0 | 0.5.1 | YES | dev-dependency only |
| 2.1.1 | 0.5.1 | YES | dev-dependency only |

**Key finding**: criterion is a **dev-only dependency** ([dev-dependencies] in Cargo.toml). It is NOT present in production builds. Remediation tasks carry the `dev-dependency` label with Normal priority override.

## 2.5 -- Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | Action |
|--------|-----------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | Upstream backport required -- bump criterion to >= 0.5.2 |
| 2.1.x | Cargo | release/0.3.z | Upstream backport required (cross-stream, preemptive) |
