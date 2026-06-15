# Affects Versions Correction

## Current (PSIRT)

- RHTPA 2.1.0
- RHTPA 2.2.0

## Proposed

- RHTPA 2.1.0
- RHTPA 2.1.1

## Changes

### Remove: RHTPA 2.2.0

RHTPA 2.2.0 ships h2 0.4.8, which is the fixed version. It is NOT affected.

### Add: RHTPA 2.1.1

RHTPA 2.1.1 ships h2 0.4.5, which is below the fixed version 0.4.8. It IS affected but was missing from PSIRT's list.

## Rationale

Since the issue is unscoped (no stream suffix in the summary), the analysis covers all streams. Only versions that actually ship a vulnerable h2 version (< 0.4.8) should be listed in Affects Versions. The 2.2.x stream ships h2 >= 0.4.8 across all its versions, so none of those versions are affected.
