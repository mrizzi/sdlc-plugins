# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | 0.11.12 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Evidence

Lock file check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`

- **v0.3.8**: quinn-proto 0.11.9 -- vulnerable (0.11.9 < 0.11.14)
- **v0.3.12**: quinn-proto 0.11.9 -- vulnerable (0.11.9 < 0.11.14)
- **v0.4.5**: quinn-proto 0.11.9 -- vulnerable (0.11.9 < 0.11.14)
- **v0.4.8**: quinn-proto 0.11.12 -- vulnerable (0.11.12 < 0.11.14)
- **v0.4.9**: retag of v0.4.8 -- same quinn-proto 0.11.12, vulnerable
- **v0.4.11**: quinn-proto 0.11.14 -- NOT vulnerable (0.11.14 >= 0.11.14)
- **v0.4.12**: quinn-proto 0.11.14 -- NOT vulnerable (0.11.14 >= 0.11.14)

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Source Repo | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | backend | (to be checked) | Unknown |
| 2.2.x | Cargo | release/0.4.z | backend | (to be checked) | Unknown |

Note: In a live triage, the upstream fix status would be checked by running:
```
git -C /home/dev/repos/rhtpa-backend show release/0.4.z:Cargo.lock | grep -A2 'name = "quinn-proto"'
git -C /home/dev/repos/rhtpa-backend show release/0.3.z:Cargo.lock | grep -A2 'name = "quinn-proto"'
```

Based on the supportability matrix data, the latest 2.2.x builds (v0.4.11, v0.4.12) already ship quinn-proto 0.11.14, indicating the upstream fix has been incorporated into the release/0.4.z branch. For the 2.1.x stream, the latest build (v0.3.12) still ships 0.11.9, suggesting the fix has NOT been backported to release/0.3.z.

## Summary

- **2.2.x stream (scoped)**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 ship the fixed version.
- **2.1.x stream (cross-stream)**: All versions (2.1.0, 2.1.1) are affected. This is cross-stream impact -- the 2.1.x stream is outside the scope of this issue but is affected.
