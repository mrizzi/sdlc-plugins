# Step 2 -- Version Impact Analysis: CVE-2026-28940

## Fix Threshold

- Vulnerable library: serde_json
- Affected range: versions before 1.0.135
- Fix threshold: >= 1.0.135

## Version Impact Table

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

### Stream 2.2.x (issue-scoped stream)

| Version | Build Tag | serde_json version | Affected? | Notes |
|---------|-----------|--------------------|-----------|-------|
| 2.2.0   | v0.4.5    | 1.0.138            | NO        | >= 1.0.135 fix threshold |
| 2.2.1   | v0.4.8    | 1.0.138            | NO        | >= 1.0.135 fix threshold |
| 2.2.2   | v0.4.9    | --                 | NO        | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3   | v0.4.11   | 1.0.139            | NO        | >= 1.0.135 fix threshold |
| 2.2.4   | v0.4.12   | 1.0.139            | NO        | >= 1.0.135 fix threshold |

### Stream 2.1.x (cross-stream check)

| Version | Build Tag | serde_json version | Affected? | Notes |
|---------|-----------|--------------------|-----------|-------|
| 2.1.0   | v0.3.8    | 1.0.137            | NO        | >= 1.0.135 fix threshold |
| 2.1.1   | v0.3.12   | 1.0.137            | NO        | >= 1.0.135 fix threshold |

## Summary

**No supported versions are affected.** Every released version across both streams ships serde_json >= 1.0.137, which is above the fix threshold of 1.0.135. The earliest shipped version (1.0.137 in the 2.1.x stream) already includes the stack overflow fix.

The PSIRT-assigned Affects Version of "RHTPA 2.2.0" is incorrect -- version 2.2.0 ships serde_json 1.0.138, which is not vulnerable.
