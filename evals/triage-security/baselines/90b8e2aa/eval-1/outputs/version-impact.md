# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

The version impact table is built by inspecting `Cargo.lock` at the pinned
source commit (backend tag) for each version in the supportability matrix.
All versions from both supported streams (2.1.x and 2.2.x) are checked per
Important Rule 4.

| Version | Stream | Backend Tag | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-------------|-----------|-------|
| 2.1.0   | 2.1.x  | `v0.3.8`    | 0.11.9      | YES       | `git show v0.3.8:Cargo.lock` |
| 2.1.1   | 2.1.x  | `v0.3.12`   | 0.11.9      | YES       | `git show v0.3.12:Cargo.lock` |
| 2.2.0   | 2.2.x  | `v0.4.5`    | 0.11.9      | YES       | `git show v0.4.5:Cargo.lock` |
| 2.2.1   | 2.2.x  | `v0.4.8`    | 0.11.12     | YES       | `git show v0.4.8:Cargo.lock` |
| 2.2.2   | 2.2.x  | `v0.4.9`    | --          | YES       | retag of 2.2.1 (same as 2.2.1, quinn-proto 0.11.12) |
| 2.2.3   | 2.2.x  | `v0.4.11`   | 0.11.14     | NO        | `git show v0.4.11:Cargo.lock` |
| 2.2.4   | 2.2.x  | `v0.4.12`   | 0.11.14     | NO        | `git show v0.4.12:Cargo.lock` |

**Fix threshold**: 0.11.14 (from CVE description; versions < 0.11.14 are affected)

**Retag handling (Important Rule 5)**: Version 2.2.2 (build 0.4.9) is a retag of
2.2.1 (build 0.4.8) per the supportability matrix note "backend retag of 2.2.1".
The lock file check is skipped for 2.2.2 and the result from 2.2.1 (quinn-proto
0.11.12, affected) is carried forward.

**Pinned commit evidence (Important Rule 13)**: Each version's quinn-proto version
is extracted using the exact backend tag from the supportability matrix via
`git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`, not branch HEAD.

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto (Cargo):
  Ecosystem: Cargo (source dependency)
  Lock file: Cargo.lock
  Profile: production (runtime dependency)

  quinn-proto is present in all versions across both streams (2.1.x and 2.2.x),
  indicating it was introduced before version 2.1.0.

  Versions shipping vulnerable quinn-proto (< 0.11.14):
    2.1.0, 2.1.1: quinn-proto 0.11.9
    2.2.0: quinn-proto 0.11.9
    2.2.1, 2.2.2: quinn-proto 0.11.12

  Versions shipping fixed quinn-proto (>= 0.11.14):
    2.2.3, 2.2.4: quinn-proto 0.11.14
```

## Upstream Fix Status (Step 2.5)

The upstream fix status is checked by inspecting the dependency version at the
upstream branch HEAD for each affected stream's Ecosystem Mappings Upstream Branch.

| Stream | Ecosystem | Upstream Branch | Check Command | Notes |
|--------|-----------|-----------------|---------------|-------|
| 2.1.x  | Cargo     | `release/0.3.z` | `git show release/0.3.z:Cargo.lock` | Upstream branch from 2.1.x Ecosystem Mappings |
| 2.2.x  | Cargo     | `release/0.4.z` | `git show release/0.4.z:Cargo.lock` | Upstream branch from 2.2.x Ecosystem Mappings |

The latest released versions in the 2.2.x stream (2.2.3, 2.2.4) already ship
quinn-proto 0.11.14, which is the fixed version. This indicates the upstream fix
has already been applied to the `release/0.4.z` branch.

For the 2.1.x stream, both released versions (2.1.0, 2.1.1) ship quinn-proto
0.11.9, indicating the fix has not been applied to the `release/0.3.z` branch.
