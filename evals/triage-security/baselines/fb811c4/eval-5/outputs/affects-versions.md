# Affects Versions Correction — TC-8005 (CVE-2026-40215)

## Current State

The issue currently has:
- **Affects Versions**: RHTPA 2.0.0

This is incorrect. RHTPA 2.0.0 is not in the 2.2.x stream and the version impact analysis shows that the affected versions within the 2.2.x stream are 2.2.0, 2.2.1, and 2.2.2.

## Proposed Correction

**Replace** the current Affects Versions with:

- RHTPA 2.2.0
- RHTPA 2.2.1
- RHTPA 2.2.2

## Rationale

Based on the version impact analysis for the 2.2.x stream:

| Version | openssl-libs | Affected |
|---------|-------------|----------|
| RHTPA 2.2.0 | 3.0.7-25.el9_3 | YES -- below fixed version 3.0.7-28.el9_4 |
| RHTPA 2.2.1 | 3.0.7-27.el9_4 | YES -- below fixed version 3.0.7-28.el9_4 |
| RHTPA 2.2.2 | 3.0.7-27.el9_4 | YES -- retag of 2.2.1, same version |
| RHTPA 2.2.3 | 3.0.7-28.el9_4 | NO -- at or above fixed version |
| RHTPA 2.2.4 | 3.0.7-28.el9_4 | NO -- at or above fixed version |

Versions 2.2.3 and 2.2.4 already include the fixed openssl-libs version (3.0.7-28.el9_4) and are therefore not affected.

## Action

Proposal: Update the Affects Versions field on TC-8005 from "RHTPA 2.0.0" to "RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2" using the Jira version names with the RHTPA prefix as defined in the supportability matrix.
