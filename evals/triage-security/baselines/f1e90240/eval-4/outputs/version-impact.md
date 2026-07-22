# Step 2 -- Version Impact Analysis: CVE-2026-33501

## Version Impact Table

CVE-2026-33501 affects h2 versions before 0.4.8. Fix threshold: **h2 >= 0.4.8**.

| Version | Stream | Build Tag | h2 version | Affected? | Notes |
|---------|--------|-----------|------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.4.5 | **YES** | < 0.4.8 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.4.5 | **YES** | < 0.4.8 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.4.8 | NO | = 0.4.8 (fixed version) |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.4.8 | NO | = 0.4.8 (fixed version) |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.4.9 | NO | > 0.4.8 |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.4.9 | NO | > 0.4.8 |

## Stream Impact Summary

| Stream | Affected? | Affected Versions | Unaffected Versions |
|--------|-----------|-------------------|---------------------|
| 2.1.x | **YES** | 2.1.0, 2.1.1 | _(none)_ |
| 2.2.x | NO | _(none)_ | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 |

The vulnerability has **mixed impact across streams**: the 2.1.x stream ships h2 0.4.5 (vulnerable), while the 2.2.x stream ships h2 >= 0.4.8 (patched). Only the 2.1.x stream requires remediation.

## Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: source dependency (Cargo crate)
  Profile: production (h2 is a runtime dependency for HTTP/2 support)
  Ecosystem: Cargo
  Lock file: Cargo.lock

  Stream 2.1.x: h2 0.4.5 -- VULNERABLE (< 0.4.8)
  Stream 2.2.x: h2 0.4.8+ -- FIXED (>= 0.4.8)

Remediation: bump h2 to >= 0.4.8 in Cargo.toml / Cargo.lock on release/0.3.z
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Threshold | Status |
|--------|-----------|-----------------|---------------|--------|
| 2.1.x | Cargo | release/0.3.z | h2 >= 0.4.8 | Needs upstream backport -- 2.1.x ships h2 0.4.5 |
| 2.2.x | Cargo | release/0.4.z | h2 >= 0.4.8 | Already fixed -- 2.2.x ships h2 >= 0.4.8 |

The upstream fix PR is [hyperium/h2#812](https://github.com/hyperium/h2/pull/812). The fix adds a configurable maximum header list size defaulting to 16 KiB.
