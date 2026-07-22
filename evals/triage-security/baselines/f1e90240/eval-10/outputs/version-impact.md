# Version Impact Analysis — CVE-2026-55123 (tokio < 1.42.0)

## Version Impact Table

| Version     | Stream    | tokio version | Affected? | Notes |
|-------------|-----------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0        | YES       |       |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0        | YES       |       |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1        | YES       |       |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1        | YES       |       |

All supported versions across both streams ship tokio < 1.42.0 and are affected.

## Cross-Stream Impact

This issue is scoped to stream **rhtpa-2.2** (suffix `[rhtpa-2.2]`).

- **rhtpa-2.2** (in scope): RHTPA 2.2.0 and 2.2.1 are affected (tokio 1.41.1 < 1.42.0)
- **rhtpa-2.1** (out of scope): RHTPA 2.1.0 and 2.1.1 are also affected (tokio 1.40.0 < 1.42.0)

Stream rhtpa-2.1 is affected but falls outside the issue's stream scope. A JQL search for sibling CVE Jiras with label `CVE-2026-55123` returns **no results** for stream rhtpa-2.1 — no CVE Jira exists for that stream. This triggers **Case B** (cross-stream preemptive remediation).

## Affects Versions Correction (Step 3)

Scoped to stream rhtpa-2.2 only:

- Current Affects Versions: `[RHTPA 2.2.0, RHTPA 2.2.1]`
- Proposed Affects Versions: `[RHTPA 2.2.0, RHTPA 2.2.1]`
- **No correction needed** — PSIRT-assigned Affects Versions are correct for the scoped stream.

## Sibling/Duplicate Check (Step 4)

- JQL search for sibling Vulnerability issues with label `CVE-2026-55123`: **no results**
- No same-stream duplicates found
- No cross-stream companion CVE Jiras found (rhtpa-2.1 has none)
