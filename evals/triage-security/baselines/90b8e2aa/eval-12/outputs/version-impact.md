# Step 2 -- Version Impact Analysis

## Enriched Fix Threshold

From Step 1.5 external CVE data enrichment:
- Library: h2
- Fix threshold: **0.4.8** (versions < 0.4.8 are affected)
- Source: MITRE CVE API and OSV.dev (cross-validated, in agreement)

## Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | h2 Version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.1 | v0.3.12 | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |

### Stream 2.2.x (rhtpa-release.0.4.z) -- issue scope

| Version | Build Tag | h2 Version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (fixed) |
| 2.2.1 | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (fixed) |
| 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 (fixed) |
| 2.2.4 | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 (fixed) |

## Impact Summary

**Issue-scoped stream (2.2.x): NO versions affected.**

All 2.2.x versions ship h2 >= 0.4.8, which is at or above the fix threshold. The earliest 2.2.x version (2.2.0, build v0.4.5) already includes h2 0.4.8 -- the fixed version. The vulnerability was never present in any shipped 2.2.x release.

**Cross-stream impact (2.1.x): ALL versions affected.**

Both 2.1.x versions (2.1.0 and 2.1.1) ship h2 0.4.5, which is below the fix threshold of 0.4.8. The 2.1.x stream is tracked by a separate Konflux release repo (rhtpa-release.0.3.z) and would require its own CVE Jira for remediation.

## Dependency Chain Context

h2 is a Cargo (Rust) dependency in the backend repository. Based on the Ecosystem Mappings, the check command is `git show <tag>:Cargo.lock` against the backend repository.

For the 2.1.x stream (affected versions):
- h2 0.4.5 is present in Cargo.lock at both v0.3.8 and v0.3.12
- h2 is a source dependency (Cargo ecosystem)
- Upstream branch: `release/0.3.z` (from 2.1.x Ecosystem Mappings)

For the 2.2.x stream (not affected):
- h2 0.4.8+ is present in Cargo.lock at all 2.2.x build tags
- The fix was already incorporated before the first 2.2.x release

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | h2 at HEAD | Fixed? |
|--------|-----------|-----------------|------------|--------|
| 2.1.x | Cargo | release/0.3.z | (not checked -- 2.1.x outside issue scope) | Unknown |
| 2.2.x | Cargo | release/0.4.z | 0.4.9 (per latest build v0.4.12) | YES |

## Triage Outcome for TC-8030

Since TC-8030 is scoped to stream 2.2.x via the summary suffix `[rhtpa-2.2]`, and **no 2.2.x versions are affected**, this is **Case C: No supported versions affected**.

Recommendation: Close TC-8030 as "Not a Bug" with VEX Justification "Vulnerable Code not Present" -- h2 is shipped in all 2.2.x versions but at version 0.4.8+, which contains the fix. The vulnerable code path from CVE-2026-48901 is not present in the shipped versions.

Cross-stream note: The 2.1.x stream IS affected (h2 0.4.5 < 0.4.8 in both 2.1.0 and 2.1.1). If no companion CVE Jira exists for the 2.1.x stream, PSIRT should be notified to create one, or preemptive remediation tasks should be created for the 2.1.x stream.
