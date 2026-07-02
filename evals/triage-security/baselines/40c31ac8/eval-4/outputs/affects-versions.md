# Affects Versions Correction -- TC-8004

## Current vs Proposed

| | Versions |
|---|---|
| **Current** (PSIRT-assigned) | RHTPA 2.1.0, RHTPA 2.2.0 |
| **Proposed** (lock file evidence) | RHTPA 2.1.0, RHTPA 2.1.1 |

## Changes

| Action | Version | Reason |
|--------|---------|--------|
| **Keep** | RHTPA 2.1.0 | Affected -- ships h2 0.4.5 (vulnerable, < 0.4.8) |
| **Add** | RHTPA 2.1.1 | Affected -- ships h2 0.4.5 (vulnerable, < 0.4.8); missing from PSIRT assignment |
| **Remove** | RHTPA 2.2.0 | NOT affected -- ships h2 0.4.8 (fixed version); incorrectly included by PSIRT |

## Rationale

The PSIRT-assigned Affects Versions included RHTPA 2.2.0, but lock file analysis at the pinned source commit (v0.4.5) shows that version 2.2.0 ships h2 0.4.8, which is the fixed version. RHTPA 2.2.0 is therefore not affected by CVE-2026-33501.

Conversely, RHTPA 2.1.1 was missing from the PSIRT assignment despite shipping h2 0.4.5 (vulnerable). It must be added to the Affects Versions.

This correction is scoped to **affected versions only** -- only versions that ship h2 < 0.4.8 (the fix threshold) are included. Since the issue is unscoped (no stream suffix), all streams were evaluated, but only 2.1.x versions are actually affected.

## Proposed Jira Update

```
jira.edit_issue("TC-8004", fields={
  "versions": [
    {"name": "RHTPA 2.1.0"},
    {"name": "RHTPA 2.1.1"}
  ]
})
```

## Correction Comment

```
Corrected Affects Versions: [RHTPA 2.1.0, RHTPA 2.2.0] -> [RHTPA 2.1.0, RHTPA 2.1.1].

Based on lock file analysis at pinned commits from security-matrix.md:
- RHTPA 2.1.0 (v0.3.8): h2 0.4.5 -- AFFECTED
- RHTPA 2.1.1 (v0.3.12): h2 0.4.5 -- AFFECTED (added)
- RHTPA 2.2.0 (v0.4.5): h2 0.4.8 -- NOT AFFECTED (removed)

Issue is unscoped -- all streams evaluated. Only 2.1.x versions are affected.
```
