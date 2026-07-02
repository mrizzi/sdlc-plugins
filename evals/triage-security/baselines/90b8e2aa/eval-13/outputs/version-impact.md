# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8, quinn-proto 0.11.12) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Dependency Chain Context (Step 2.3.5)

quinn-proto is a source-level Cargo dependency.

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn -> quinn-proto
  Profile: production (quinn is a runtime dependency)

  Present in: all versions across both streams (2.1.x and 2.2.x)
  Direct dependency: No (transitive via quinn crate)
```

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (at v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (at v0.4.12) | YES |

### Analysis

- **2.2.x stream**: Fix is already present. Versions 2.2.3+ (build tags v0.4.11+) ship quinn-proto 0.11.14, which is the fixed version. The upstream branch `release/0.4.z` already has the fix. No remediation task needed for this stream.
- **2.1.x stream**: All versions (2.1.0, 2.1.1) ship quinn-proto 0.11.9, which is vulnerable. The upstream branch `release/0.3.z` does NOT have the fix -- the latest tag (v0.3.12) still uses quinn-proto 0.11.9. Remediation is required: upstream backport to `release/0.3.z` followed by downstream propagation in `rhtpa-release.0.3.z`.

## Affects Versions Correction (Step 3)

Issue is scoped to stream 2.2.x. Only 2.2.x versions are proposed for Affects Versions:

```
Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

RHTPA 2.0.0 does not exist as a configured version stream. The affected 2.2.x versions based on lock file evidence are 2.2.0, 2.2.1, and 2.2.2. Versions 2.2.3 and 2.2.4 are NOT affected (they ship the fix).

## Cross-Stream Impact (Case B)

Stream 2.1.x is also affected (all versions ship quinn-proto 0.11.9) but is outside this issue's scope. No sibling CVE Jira exists for the 2.1.x stream (would need to verify via JQL search). Preemptive remediation tasks should be created for the 2.1.x stream per Case B.
