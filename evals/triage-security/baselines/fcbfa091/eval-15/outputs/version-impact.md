# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0   | 0.11.9      | YES       |       |
| 2.1.1   | 0.11.9      | YES       |       |
| 2.2.0   | 0.11.9      | YES       |       |
| 2.2.1   | 0.11.12     | YES       |       |
| 2.2.2   | --          | YES       | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3   | 0.11.14     | NO        |       |
| 2.2.4   | 0.11.14     | NO        |       |

## Stream Summary

| Stream | Versions Affected | Versions Not Affected |
|--------|-------------------|-----------------------|
| 2.1.x  | 2.1.0, 2.1.1     | --                    |
| 2.2.x  | 2.2.0, 2.2.1, 2.2.2 | 2.2.3, 2.2.4      |

## Evidence

Dependency versions extracted from `Cargo.lock` at pinned source commits per security-matrix.md:

| Tag | quinn-proto version | Fix threshold (0.11.14) | Result |
|-----|---------------------|-------------------------|--------|
| v0.3.8  | 0.11.9  | < 0.11.14 | AFFECTED |
| v0.3.12 | 0.11.9  | < 0.11.14 | AFFECTED |
| v0.4.5  | 0.11.9  | < 0.11.14 | AFFECTED |
| v0.4.8  | 0.11.12 | < 0.11.14 | AFFECTED |
| v0.4.9  | _(retag of v0.4.8)_ | same as 2.2.1 | AFFECTED |
| v0.4.11 | 0.11.14 | >= 0.11.14 | NOT AFFECTED |
| v0.4.12 | 0.11.14 | >= 0.11.14 | NOT AFFECTED |

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.1.x  | Cargo     | release/0.3.z   | Fix available -- quinn-proto 0.11.14 released upstream |
| 2.2.x  | Cargo     | release/0.4.z   | Fixed in v0.4.11+ (ships quinn-proto 0.11.14) |
