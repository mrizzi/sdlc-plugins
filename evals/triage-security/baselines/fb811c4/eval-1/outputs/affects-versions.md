# Step 3: Affects Versions Correction

## Current State

The Vulnerability issue TC-8001 currently has:

- **Affects Versions**: RHTPA 2.0.0

## Problem

The PSIRT-assigned Affects Versions value of **RHTPA 2.0.0** is incorrect. Lock-file verification against the supportability matrix shows that RHTPA 2.0.0 does not appear in any supported version stream. The actual affected versions, determined by checking the quinn-proto dependency version at each pinned commit tag, are different.

## Lock-File-Verified Impact

Based on the version impact analysis:

| Version | quinn-proto | Affected? | Stream |
|---------|-------------|-----------|--------|
| RHTPA 2.1.0 | 0.11.9 | YES | 2.1.x |
| RHTPA 2.1.1 | 0.11.9 | YES | 2.1.x |
| RHTPA 2.2.0 | 0.11.9 | YES | 2.2.x |
| RHTPA 2.2.1 | 0.11.12 | YES | 2.2.x |
| RHTPA 2.2.2 | 0.11.12 | YES | 2.2.x |
| RHTPA 2.2.3 | 0.11.14 | NO | 2.2.x |
| RHTPA 2.2.4 | 0.11.14 | NO | 2.2.x |

## Stream Scope

The issue summary contains the stream suffix `[rhtpa-2.2]`, which scopes this Vulnerability issue to the **2.2.x stream only**. Versions in the 2.1.x stream (RHTPA 2.1.0, RHTPA 2.1.1), while also affected by the vulnerability, are outside the scope of this issue and would be tracked under a separate `[rhtpa-2.1]` Vulnerability issue if applicable.

Within the 2.2.x stream, the affected versions are those where quinn-proto < 0.11.14:
- **RHTPA 2.2.0** (quinn-proto 0.11.9)
- **RHTPA 2.2.1** (quinn-proto 0.11.12)
- **RHTPA 2.2.2** (quinn-proto 0.11.12, retag of 2.2.1)

Versions RHTPA 2.2.3 and RHTPA 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are NOT affected.

## Proposed Correction

**PROPOSAL** (requires confirmation before execution):

- **Remove**: RHTPA 2.0.0 (not a valid version in the supportability matrix)
- **Add**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

The corrected Affects Versions field for TC-8001 would be:

> **Affects Versions**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

This proposal uses Jira version names with the configured version prefix "RHTPA" as specified in the project's Security Configuration. The actual Jira update should match these version names to the corresponding Jira version objects in the TC project.
