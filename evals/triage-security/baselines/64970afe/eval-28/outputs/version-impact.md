# Step 2 -- Version Impact Analysis for TC-8060

CVE-2026-99010: h2 (versions before 0.4.5, fixed in 0.4.5)

## 2.1 -- Supportability Matrix (2.2.x stream, scoped)

Loaded from: security-matrix-mock.md (2.2.x stream section)
Last-Updated: 2026-06-28T10:00:00Z (11 days ago -- within 14-day freshness threshold)

| Version | Build | Build Date | Backend Tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | |

## 2.3 -- Dependency Version Extraction

Ecosystem: Cargo
Lock file: Cargo.lock
Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`

Extracted h2 versions from lock file evidence:

| Backend Tag | h2 Version | Source |
|-------------|------------|--------|
| v0.4.5 | 0.4.4 | Cargo.lock at v0.4.5 |
| v0.4.8 | 0.4.4 | Cargo.lock at v0.4.8 |
| v0.4.8 (retag) | 0.4.4 | same as v0.4.8 |
| v0.4.11 | 0.4.5 | Cargo.lock at v0.4.11 |
| v0.4.12 | 0.4.5 | Cargo.lock at v0.4.12 |

Fix threshold: h2 >= 0.4.5 (from Jira description; enriched fix threshold from Step 1.5 would cross-validate against MITRE CVE API and OSV.dev).

## 2.3.5 -- Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> reqwest -> hyper -> h2
  Type: transitive (3 levels deep)
  Profile: production (reqwest is a runtime dependency)

First appeared: 2.1.0 (initial project setup -- reqwest has always depended on hyper/h2)
Present in all versions
```

Manifest evidence:
```toml
# backend/Cargo.toml (all versions)
[dependencies]
reqwest = { version = "0.12", features = ["json"] }
# h2 is NOT a direct dependency -- it comes through reqwest -> hyper -> h2
```

Lock file evidence (affected versions -- 2.2.0 through 2.2.2):
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

Lock file evidence (fixed versions -- 2.2.3+):
```
[[package]]
name = "h2"
version = "0.4.5"
```

Remediation approach: bump reqwest if a version with fixed h2 (>= 0.4.5) is available; otherwise pin h2 directly via `cargo add h2@0.4.5`.

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-99010 (h2 < 0.4.5):

| Version | h2 Version | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.2.0 | 0.4.4 | YES | < 0.4.5 |
| 2.2.1 | 0.4.4 | YES | < 0.4.5 |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.4.5 | NO | = 0.4.5 (fixed version) |
| 2.2.4 | 0.4.5 | NO | = 0.4.5 (fixed version) |

Affected versions: 2.2.0, 2.2.1, 2.2.2
Not affected versions: 2.2.3, 2.2.4

Dependency chain: backend -> reqwest -> hyper -> h2 (transitive, 3 levels deep, production profile)

## 2.5 -- Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | h2 at HEAD | Fixed? |
|--------|-----------|-----------------|------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.4.5 | YES |

The upstream branch release/0.4.z already contains h2 0.4.5 (the fix). Remediation for the 2.2.x stream is a Konflux release repo change: bump the source tag/commit reference to pick up the fix that is already present in versions 2.2.3+.

## Cross-Stream Impact Check (for Step 8 Case B)

The 2.1.x stream was also checked for cross-stream impact:

| Version | Backend Tag | h2 Version | Affected? |
|---------|-------------|------------|-----------|
| 2.1.0 | v0.3.8 | 0.4.5 | NO |
| 2.1.1 | v0.3.12 | 0.4.5 | NO |

The 2.1.x stream is NOT affected -- all versions ship h2 >= 0.4.5. No cross-stream remediation needed.
