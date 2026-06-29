# Step 3 — Affects Versions Correction

## Current vs. Corrected

| | Value |
|---|---|
| **Current Affects Versions** (PSIRT-assigned) | RHTPA 2.0.0 |
| **Corrected Affects Versions** (from lock file evidence) | RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 |

## Rationale

PSIRT assigned **RHTPA 2.0.0** as the Affects Version, but this is incorrect:

1. **No 2.0.x stream exists** — the configured Version Streams are 2.1.x and 2.2.x.
   There is no Konflux release repo for a 2.0.x stream, so RHTPA 2.0.0 is not a
   valid affected version.

2. **This issue is scoped to the 2.2.x stream** (per summary suffix `[rhtpa-2.2]`).
   Only versions within that stream should be listed in Affects Versions.

3. **Lock file evidence** from `rpms.lock.yaml` shows:
   - **2.2.0** ships openssl-libs 3.0.7-25.el9_3 — AFFECTED (before 3.0.7-28.el9_4)
   - **2.2.1** ships openssl-libs 3.0.7-27.el9_4 — AFFECTED (before 3.0.7-28.el9_4)
   - **2.2.2** ships openssl-libs 3.0.7-27.el9_4 — AFFECTED (retag of 2.2.1, same version)
   - **2.2.3** ships openssl-libs 3.0.7-28.el9_4 — NOT affected (fixed version)
   - **2.2.4** ships openssl-libs 3.0.7-28.el9_4 — NOT affected (fixed version)

## Proposed Jira Mutation

Remove RHTPA 2.0.0 and set Affects Versions to: **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2**.

This correction would be performed after engineer confirmation using dynamic version
discovery via `getJiraIssueTypeMetaWithFields` to resolve the correct Jira version IDs.
