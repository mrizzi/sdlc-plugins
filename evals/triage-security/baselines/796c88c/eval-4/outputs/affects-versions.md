# Affects Versions Correction — TC-8004

## Current Affects Versions (as filed)

- RHTPA 2.1.0
- RHTPA 2.2.0

## Problem

The current Affects Versions list includes **RHTPA 2.2.0**, but version impact analysis shows that RHTPA 2.2.0 ships h2 0.4.8 (the fixed version) and is **NOT affected**. Additionally, **RHTPA 2.1.1** is missing but IS affected (ships h2 0.4.5).

## Proposed Affects Versions Correction

**Remove**: RHTPA 2.2.0 (ships h2 0.4.8 — not vulnerable)
**Add**: RHTPA 2.1.1 (ships h2 0.4.5 — vulnerable)

### Corrected Affects Versions

- **RHTPA 2.1.0** (h2 0.4.5 — affected)
- **RHTPA 2.1.1** (h2 0.4.5 — affected)

## Rationale

Since the issue is **UNSCOPED**, the Affects Versions field should include all affected versions across all streams. The version impact analysis confirmed:

- 2.1.x stream: ALL versions affected (h2 0.4.5 < 0.4.8)
- 2.2.x stream: NO versions affected (h2 >= 0.4.8)

Only versions that actually ship the vulnerable dependency should be listed.

## Proposed Jira Mutation

```
Update TC-8004 Affects Versions:
  Remove: RHTPA 2.2.0
  Add:    RHTPA 2.1.1
  Result: [RHTPA 2.1.0, RHTPA 2.1.1]
```

**Status**: PROPOSAL — not yet executed.
