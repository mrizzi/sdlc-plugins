# Version Impact Analysis — TC-8020

## Fix Threshold

- **Vulnerable library**: tokio
- **Affected range**: versions before 1.42.0
- **Fixed version**: 1.42.0

## Version Impact Table

| Version | Stream | Build Tag | tokio version | Affected? | Notes |
|---------|--------|-----------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | v0.3.8 | 1.40.0 | YES | 1.40.0 < 1.42.0 |
| RHTPA 2.1.1 | rhtpa-2.1 | v0.3.12 | 1.40.0 | YES | 1.40.0 < 1.42.0 |
| RHTPA 2.2.0 | rhtpa-2.2 | v0.4.5 | 1.41.1 | YES | 1.41.1 < 1.42.0 |
| RHTPA 2.2.1 | rhtpa-2.2 | v0.4.8 | 1.41.1 | YES | 1.41.1 < 1.42.0 |

## Cross-Stream Impact Summary

The issue is scoped to stream **rhtpa-2.2** (2.2.x), but the version impact analysis reveals that stream **rhtpa-2.1** (2.1.x) is also affected:

- **rhtpa-2.2** (in scope): All versions (RHTPA 2.2.0, RHTPA 2.2.1) ship tokio 1.41.1, which is below the fix threshold of 1.42.0. **AFFECTED.**
- **rhtpa-2.1** (out of scope): All versions (RHTPA 2.1.0, RHTPA 2.1.1) ship tokio 1.40.0, which is below the fix threshold of 1.42.0. **AFFECTED.**

## Sibling CVE Jira Search

A JQL search for sibling CVE Jiras with label `CVE-2026-55123` in stream `rhtpa-2.1` returned **no results**. No CVE Jira exists for stream rhtpa-2.1.

This triggers **Case B** (cross-stream preemptive remediation) for the rhtpa-2.1 stream.
