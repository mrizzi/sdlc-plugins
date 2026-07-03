# Step 2 -- Version Impact Analysis for CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | 0.11.14 | NO | |

## Dependency Chain Context

Dependency chain for quinn-proto (Cargo):
- Ecosystem: Cargo (Rust crate)
- Lock file: `Cargo.lock`
- Source repository: rhtpa-backend

quinn-proto is present in Cargo.lock for all versions checked. Versions 2.2.0 through 2.2.2 ship quinn-proto < 0.11.14 (the fix threshold). Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (at or above the fix threshold).

Stream 2.1.x (versions 2.1.0, 2.1.1) also ships quinn-proto 0.11.9, which is within the affected range. This is outside the current issue's stream scope but represents cross-stream impact (Case B).

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.1.x | Cargo | release/0.3.z | Upstream fix PR: quinn-rs/quinn#2048 |
| 2.2.x | Cargo | release/0.4.z | Upstream fix PR: quinn-rs/quinn#2048 |

Upstream fix PR available: https://github.com/quinn-rs/quinn/pull/2048
