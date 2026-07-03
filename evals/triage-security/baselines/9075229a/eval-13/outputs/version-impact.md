# Step 2 -- Version Impact Analysis for TC-8001

## 2.1 -- Supportability Matrix

Loaded from two configured Version Streams:

- **2.1.x** stream: security-matrix.md at `/home/dev/repos/rhtpa-release.0.3.z` (Last-Updated: 2026-06-28T10:00:00Z -- 5 days ago, within 14-day threshold)
- **2.2.x** stream: security-matrix.md at `/home/dev/repos/rhtpa-release.0.4.z` (Last-Updated: 2026-06-28T10:00:00Z -- 5 days ago, within 14-day threshold)

## 2.3 -- Dependency Version Extraction

quinn-proto versions extracted via `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'` for each pinned commit:

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Tag | quinn-proto version | Comparison vs fix (0.11.14) |
|---------|-----|---------------------|-----------------------------|
| 2.1.0 | v0.3.8 | 0.11.9 | < 0.11.14 -- AFFECTED |
| 2.1.1 | v0.3.12 | 0.11.9 | < 0.11.14 -- AFFECTED |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Tag | quinn-proto version | Comparison vs fix (0.11.14) |
|---------|-----|---------------------|-----------------------------|
| 2.2.0 | v0.4.5 | 0.11.9 | < 0.11.14 -- AFFECTED |
| 2.2.1 | v0.4.8 | 0.11.12 | < 0.11.14 -- AFFECTED |
| 2.2.2 | v0.4.9 | (retag of v0.4.8) | same as 2.2.1 -- AFFECTED |
| 2.2.3 | v0.4.11 | 0.11.14 | >= 0.11.14 -- NOT AFFECTED |
| 2.2.4 | v0.4.12 | 0.11.14 | >= 0.11.14 -- NOT AFFECTED |

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | 0.11.14 | NO | |

### Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) -> reqwest [features: http3] -> h3 -> quinn -> quinn-proto
  Profile: production (reqwest is a runtime dependency)

  First appeared: 2.1.0 (tag v0.3.8)
  Present in all versions across both streams.
```

## 2.5 -- Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 | NO |

- **2.2.x (release/0.4.z)**: Fixed upstream. Versions 2.2.3+ already ship 0.11.14. Remediation for affected versions (2.2.0-2.2.2) involves updating the source reference in the Konflux release repo to a commit that includes the fix.
- **2.1.x (release/0.3.z)**: NOT fixed upstream. Remediation requires an upstream PR to bump quinn-proto on the release/0.3.z branch first, then a downstream propagation.

## Summary of Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions of `RHTPA 2.0.0` is incorrect. There is no 2.0.x stream configured. Based on lock file evidence, the correct Affects Versions for the scoped 2.2.x stream are:

- **Remove**: RHTPA 2.0.0 (no 2.0.x stream exists)
- **Add**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

Versions RHTPA 2.2.3 and RHTPA 2.2.4 are NOT affected (ship quinn-proto 0.11.14, which is the fix version).
