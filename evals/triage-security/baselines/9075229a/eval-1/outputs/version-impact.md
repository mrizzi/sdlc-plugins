# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | at fix version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | at fix version |

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) -> quinn -> quinn-proto
  Profile: production (quinn is a runtime dependency)
  Ecosystem: Cargo (source dependency)
```

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Repository | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|------------|-----------------|-----------------|--------|
| 2.1.x | Cargo | backend | release/0.3.z | -- | requires inspection |
| 2.2.x | Cargo | backend | release/0.4.z | 0.11.14 | YES |

Based on the version impact table:
- **Stream 2.2.x** (issue scope): versions 2.2.0, 2.2.1, 2.2.2 are affected; versions 2.2.3 and 2.2.4 already ship the fix.
- **Stream 2.1.x** (outside issue scope): versions 2.1.0 and 2.1.1 are affected -- cross-stream impact detected (Case B).
