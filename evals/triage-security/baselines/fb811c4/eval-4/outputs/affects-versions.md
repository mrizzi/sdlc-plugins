# Step 3: Affects Versions Correction

## Current State

The issue TC-8004 currently has:

- **Affects Versions**: RHTPA 2.1.0, RHTPA 2.2.0

## Proposed Correction

Based on the version impact analysis, the Affects Versions field should be corrected to include only actually affected versions.

### Versions to keep

- **RHTPA 2.1.0** — ships h2 0.4.5, which is vulnerable (< 0.4.8)

### Versions to add

- **RHTPA 2.1.1** — ships h2 0.4.5, which is vulnerable (< 0.4.8). This version was missing from the original Affects Versions and should be added.

### Versions to remove

- **RHTPA 2.2.0** — ships h2 0.4.8, which is the fixed version. This version is NOT affected and should be removed.

## Corrected Affects Versions

**RHTPA 2.1.0, RHTPA 2.1.1**

## Jira Update Proposal

Use Jira version names from the supportability matrix with the Jira version prefix `RHTPA`:

1. Remove version `RHTPA 2.2.0` from the Affects Versions field
2. Add version `RHTPA 2.1.1` to the Affects Versions field
3. Retain version `RHTPA 2.1.0` (already present and correct)

The version names are derived from the supportability matrix Version column prefixed with the Jira version prefix `RHTPA` from the Security Configuration.
