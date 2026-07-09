# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto versions before 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same backend tag v0.4.8) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

## Evidence

Fix threshold: >= 0.11.14 (from Jira description and CVE record).

Lock file versions were extracted via `git show <tag>:Cargo.lock` for each backend tag in the supportability matrix:

- `v0.3.8` (2.1.0): quinn-proto 0.11.9 -- AFFECTED (< 0.11.14)
- `v0.3.12` (2.1.1): quinn-proto 0.11.9 -- AFFECTED (< 0.11.14)
- `v0.4.5` (2.2.0): quinn-proto 0.11.9 -- AFFECTED (< 0.11.14)
- `v0.4.8` (2.2.1): quinn-proto 0.11.12 -- AFFECTED (< 0.11.14)
- `v0.4.9` (2.2.2): retag of v0.4.8 -- same as 2.2.1 (quinn-proto 0.11.12, AFFECTED)
- `v0.4.11` (2.2.3): quinn-proto 0.11.14 -- NOT AFFECTED (>= 0.11.14)
- `v0.4.12` (2.2.4): quinn-proto 0.11.14 -- NOT AFFECTED (>= 0.11.14)

## Stream Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1) -- outside this issue's scope
- **2.2.x stream**: versions 2.2.0, 2.2.1, 2.2.2 affected; versions 2.2.3, 2.2.4 NOT affected (ship fixed version 0.11.14)

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Status |
|--------|-----------|-----------------|------------|
| 2.1.x | Cargo | release/0.3.z | Needs investigation |
| 2.2.x | Cargo | release/0.4.z | Fixed in v0.4.11+ (quinn-proto 0.11.14) |

The upstream fix PR is [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048). Versions 2.2.3+ already ship the fix.
