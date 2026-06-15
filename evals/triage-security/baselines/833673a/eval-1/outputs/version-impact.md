# Step 2 - Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto versions before 0.11.14):

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | 0.11.12 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | fixed version shipped |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | fixed version shipped |

## Dependency Chain Context

Dependency chain for quinn-proto (Cargo):
- Ecosystem: Cargo (source dependency)
- Lock file: `Cargo.lock`
- quinn-proto is a Rust crate used by the QUIC transport layer

The vulnerability allows a remote attacker to cause a denial of service (panic) by sending a QUIC transport frame that creates an excessive number of streams. quinn-proto before 0.11.14 does not properly validate the number of streams requested in a STREAMS frame.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix available at branch? | Notes |
|--------|-----------|-----------------|--------------------------|-------|
| 2.1.x | Cargo | release/0.3.z | Unknown | 2.1.x ships 0.11.9; needs verification at branch HEAD |
| 2.2.x | Cargo | release/0.4.z | YES | v0.4.11+ already ships 0.11.14 (the fixed version) |

## Cross-Stream Impact

- **2.1.x stream**: versions 2.1.0 and 2.1.1 are AFFECTED (quinn-proto 0.11.9)
- **2.2.x stream**: versions 2.2.0, 2.2.1, and 2.2.2 are AFFECTED; versions 2.2.3 and 2.2.4 are NOT affected (ship 0.11.14)

Since this issue is scoped to the 2.2.x stream, the 2.1.x impact is noted as cross-stream impact for a companion PSIRT issue.
