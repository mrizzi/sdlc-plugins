# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-55123 (tokio < 1.42.0)

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES | |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES | |

All versions across both streams ship tokio < 1.42.0 and are therefore affected.

## Cross-Stream Impact Summary

- **Current issue stream (rhtpa-2.2)**: RHTPA 2.2.0, RHTPA 2.2.1 -- both affected (tokio 1.41.1)
- **Other stream (rhtpa-2.1)**: RHTPA 2.1.0, RHTPA 2.1.1 -- both affected (tokio 1.40.0)

Stream rhtpa-2.1 is outside the scope of TC-8020 (which is scoped to rhtpa-2.2) but is also affected. This triggers Case B (cross-stream impact) in Step 8.

## Sibling CVE Jira Search

JQL: `project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020`

**Result**: No sibling Vulnerability issues found for CVE-2026-55123 in stream rhtpa-2.1. No CVE Jira exists for the rhtpa-2.1 stream.

## Fix Threshold

- Fixed version: **1.42.0** (from Jira description)
- All shipped versions (1.40.0 in 2.1.x, 1.41.1 in 2.2.x) are below the fix threshold
