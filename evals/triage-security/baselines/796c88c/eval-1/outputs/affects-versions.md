# Step 3: Affects Versions Correction

## Current State

The PSIRT-assigned Affects Versions on TC-8001:

| Current Affects Versions |
|--------------------------|
| RHTPA 2.0.0 |

## Problem

The PSIRT assigned **RHTPA 2.0.0**, which is not present in the supportability matrix and cannot be verified. The issue is scoped to the **2.2.x stream** (indicated by the `[rhtpa-2.2]` suffix in the summary), so the Affects Versions field should only include verified 2.2.x versions that are confirmed affected by lock file analysis.

## Lock-File-Verified Affected 2.2.x Versions

From the version impact analysis, the following 2.2.x versions ship a vulnerable quinn-proto (< 0.11.14):

| Version | quinn-proto | Status |
|---------|-------------|--------|
| RHTPA 2.2.0 | 0.11.9 | Affected |
| RHTPA 2.2.1 | 0.11.12 | Affected |
| RHTPA 2.2.2 | 0.11.12 (retag of 2.2.1) | Affected |

RHTPA 2.2.3 and RHTPA 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are **not affected**.

## Proposed Mutation

**Action**: Replace the Affects Versions field on TC-8001.

| Remove | Add |
|--------|-----|
| RHTPA 2.0.0 | RHTPA 2.2.0 |
| | RHTPA 2.2.1 |
| | RHTPA 2.2.2 |

**Rationale**: The Affects Versions should reflect only lock-file-verified versions within the issue's scoped stream (2.2.x). RHTPA 2.0.0 is not in the supportability matrix and belongs to a different stream. The three 2.2.x versions listed above are confirmed to ship vulnerable quinn-proto versions. Versions are referenced by name with the Jira version prefix RHTPA, not by Jira version IDs.

> **Note**: The 2.1.x stream versions (RHTPA 2.1.0, RHTPA 2.1.1) are also affected but are out of scope for this issue since it is scoped to the 2.2.x stream. A separate vulnerability issue with `[rhtpa-2.1]` suffix would cover those versions.
