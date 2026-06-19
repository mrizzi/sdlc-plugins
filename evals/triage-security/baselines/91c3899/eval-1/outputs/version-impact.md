# Step 2 -- Version Impact Analysis

## Scope

Issue TC-8001 is scoped to the **2.2.x** stream (suffix `[rhtpa-2.2]`).

Vulnerability: **CVE-2026-31812** affects quinn-proto versions **< 0.11.14**. Fixed in **0.11.14**.

## Version Impact Table -- 2.2.x Stream

All versions from the supportability matrix for the 2.2.x stream (`rhtpa-release.0.4.z`) are included below.

Dependency versions are extracted using pinned commit tags from the supportability matrix (not branch HEAD), per the rule: "Version impact evidence uses pinned commits only."

| Version | Build | Build Date | Pinned Tag | quinn-proto Version | Affected? | Notes |
|---------|-------|------------|------------|---------------------|-----------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | 0.11.12 | **YES** | 0.11.12 < 0.11.14 |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | 0.11.12 | **YES** | Retag of 2.2.1 -- same backend tag `v0.4.8`, carries forward affected status |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 (fixed version) |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 (fixed version) |

### Lock File Evidence

Each quinn-proto version was determined by simulating `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'` using the mock lock file data provided in the security matrix:

- `git show v0.4.5:Cargo.lock` --> quinn-proto **0.11.9**
- `git show v0.4.8:Cargo.lock` --> quinn-proto **0.11.12**
- `v0.4.9` is a retag of `v0.4.8` --> carries forward quinn-proto **0.11.12** (no separate lock file check needed)
- `git show v0.4.11:Cargo.lock` --> quinn-proto **0.11.14**
- `git show v0.4.12:Cargo.lock` --> quinn-proto **0.11.14**

### Retag Handling

Version **2.2.2** is identified as a retag of **2.2.1** (Notes column: "backend retag of 2.2.1"). Both share the same backend pinned tag `v0.4.8`. Per the skill rule "Handle retags explicitly", the lock file check is skipped for 2.2.2 and the affected status is carried forward from 2.2.1.

## Summary

- **Affected versions**: 2.2.0, 2.2.1, 2.2.2
- **Not affected versions**: 2.2.3, 2.2.4
- **Fix appeared in**: version 2.2.3 (build 0.4.11, tag `v0.4.11`, which ships quinn-proto 0.11.14)

## Cross-Stream Note

The 2.1.x stream (not in scope for this issue) also ships quinn-proto:
- 2.1.0 (tag `v0.3.8`): quinn-proto 0.11.9 -- would be affected
- 2.1.1 (tag `v0.3.12`): quinn-proto 0.11.9 -- would be affected

This is informational only -- the 2.1.x stream is outside the scope of this issue and would be covered by a separate PSIRT-created Vulnerability issue.
