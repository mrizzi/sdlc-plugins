# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

Scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`:

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.2.0   | v0.4.5    | 0.11.9      | YES       | < 0.11.14 |
| 2.2.1   | v0.4.8    | 0.11.12     | YES       | < 0.11.14 |
| 2.2.2   | v0.4.9    | --          | YES       | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3   | v0.4.11   | 0.11.14     | NO        | >= 0.11.14 (ships fixed version) |
| 2.2.4   | v0.4.12   | 0.11.14     | NO        | >= 0.11.14 (ships fixed version) |

Cross-stream reference (2.1.x, outside issue scope):

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.1.0   | v0.3.8    | 0.11.9      | YES       | < 0.11.14 |
| 2.1.1   | v0.3.12   | 0.11.9      | YES       | < 0.11.14 |

## Summary

Within the scoped 2.2.x stream, versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto versions below the fix threshold (0.11.14) and are affected by CVE-2026-31812. Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are NOT affected.

Cross-stream analysis shows that all 2.1.x versions (2.1.0, 2.1.1) also ship quinn-proto 0.11.9, which is within the affected range. This will be reported as cross-stream impact in Step 8 (Case B).
