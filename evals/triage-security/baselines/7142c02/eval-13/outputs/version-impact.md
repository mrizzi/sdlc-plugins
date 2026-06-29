# Step 2 -- Version Impact Analysis for CVE-2026-31812

## Version Impact Table

CVE-2026-31812 affects quinn-proto versions before 0.11.14.

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as v0.4.8, quinn-proto 0.11.12) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

## Dependency Chain Context (Step 2.3.5)

quinn-proto is a **Cargo** (Rust crate) source dependency. It is a transitive dependency brought in through the QUIC networking stack. The dependency chain is:

```
backend (workspace) -> quinn -> quinn-proto
```

Profile: production (quinn is a runtime dependency for QUIC transport).

quinn-proto is present in both streams (2.1.x and 2.2.x) across all versions inspected. The vulnerable version (< 0.11.14) was shipped from the earliest version (2.1.0 with 0.11.9) through 2.2.2 (0.11.12). The fix (0.11.14) was picked up starting at 2.2.3 (tag v0.4.11).

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | (to be checked) | unknown |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |

The 2.2.x stream upstream branch (`release/0.4.z`) already includes the fix at HEAD (v0.4.11 and v0.4.12 both ship 0.11.14). For 2.1.x, the upstream branch (`release/0.3.z`) would need to be checked, but the most recent tag (v0.3.12) still ships 0.11.9, indicating the fix has likely not been backported to the 0.3.z branch.

## Affects Versions Correction (Step 3)

The current Affects Versions on TC-8001 is "RHTPA 2.0.0". Based on version impact analysis:

- "RHTPA 2.0.0" does not correspond to any configured version stream and should be **removed**.
- Since the issue is scoped to the 2.2.x stream, the affected versions within scope are: **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2** (all ship quinn-proto < 0.11.14).
- Versions 2.2.3 and 2.2.4 are NOT affected (ship quinn-proto 0.11.14).

Proposed correction: Remove "RHTPA 2.0.0", add "RHTPA 2.2.0", "RHTPA 2.2.1", "RHTPA 2.2.2".

## Cross-Stream Impact

The 2.1.x stream is **also affected** (all versions ship quinn-proto 0.11.9, which is < 0.11.14). This is outside the current issue's scope (scoped to 2.2.x) and will be handled as Case B (cross-stream impact) in Step 7.
