# Step 2: Version Impact Analysis

## CVE-2026-31812 — quinn-proto Impact by Version

Affected condition: quinn-proto < 0.11.14

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | 0.11.12 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | |

### Methodology

- quinn-proto versions were extracted using `git show <tag>:Cargo.lock` for each pinned build tag in the supportability matrix.
- Version 2.2.2 (build 0.4.9) is a retag of 2.2.1 (build 0.4.8) with no backend source change. The quinn-proto version 0.11.12 is carried forward from 2.2.1.
- Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14, which is the fixed version, so they are NOT affected.

### Summary

- **Affected versions**: 2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2 (5 of 7 versions)
- **Not affected versions**: 2.2.3, 2.2.4 (2 of 7 versions)
- **First fixed in**: 2.2.3 (build v0.4.11)
