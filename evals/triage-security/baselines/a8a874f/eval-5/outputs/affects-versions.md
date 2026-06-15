# Affects Versions Correction (Step 3)

## Current Value (PSIRT)

- [RHTPA 2.0.0] -- incorrect; version 2.0.0 does not exist in the supportability matrix

## Proposed Value

- [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2] -- scoped to the affected 2.2.x versions only

## Rationale

The PSIRT-assigned value "RHTPA 2.0.0" does not correspond to any version in the supportability matrix. Based on the version impact analysis, versions 2.2.0, 2.2.1, and 2.2.2 ship openssl-libs versions older than the fixed 3.0.7-28.el9_4. Versions 2.2.3 and 2.2.4 already include the fix and are not affected.
