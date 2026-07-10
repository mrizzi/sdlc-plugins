# Idempotency Check -- Re-Run Analysis for TC-8001

This document analyzes all pre-existing triage artifacts detected on TC-8001
during the second invocation of triage-security, and explains why each artifact
causes the corresponding triage step to be skipped.

## Pre-Existing Artifacts Detected

### 1. Label: ai-cve-triaged

- **Detected**: The `ai-cve-triaged` label is already present on TC-8001.
- **Implication**: This label is added during the Post-Triage Summary (after Step 8).
  Its presence signals that a prior triage run completed successfully. The discovery
  mode JQL (`labels NOT IN (ai-cve-triaged)`) would exclude this issue from the
  untriaged list. When triaging by explicit issue key, the label presence serves as
  an idempotency marker -- a complete prior triage has already been executed.
- **Action**: No mutation needed. The label already exists; adding it again would
  be a no-op.

### 2. Status: In Progress

- **Detected**: TC-8001 is already in `In Progress` status (not `New` or `Assigned`).
- **Implication**: Step 0.7 transitions the issue from New to Assigned, and Step 8
  (remediation linkage) transitions it to In Progress. Since the issue is already
  past both target states, re-running these transitions is unnecessary.
- **Action**: Step 0.7 skips the transition silently (the issue is already in a
  later status than Assigned). Step 8's transition to In Progress is also a no-op
  since the issue is already In Progress. The reassignment of the issue to the
  current user still proceeds (per the skill spec -- assignment always happens
  regardless of status).

### 3. Remediation Tasks: TC-8100 and TC-8101 (linked via Depend)

- **Detected**: Two remediation tasks already linked to TC-8001 via `Depend` links:
  - **TC-8100**: "Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2]"
    (upstream backport task, status: In Progress)
  - **TC-8101**: "Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2]"
    (downstream propagation task, status: Open, blocks TC-8100)
- **Implication**: Step 8 (Case A) creates remediation tasks for affected streams.
  The existing tasks already cover the 2.2.x stream with the correct CVE
  (CVE-2026-31812), the correct library (quinn-proto), and the correct fix target
  (>= 0.11.14). Both tasks carry the expected labels (`ai-generated-jira`, `Security`,
  `CVE-2026-31812`).
- **Action**: No new remediation tasks need to be created. Creating duplicate tasks
  would produce redundant work items. The existing Depend links from TC-8001 to
  TC-8100 and TC-8101 already establish the correct traceability. The Blocks link
  from TC-8101 to TC-8100 correctly models the dependency ordering (downstream
  propagation waits for upstream backport).

### 4. Description Digest Comment

- **Detected**: Comment #1 on TC-8001 contains:
  `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2`
  Posted by sdlc-workflow/triage-security on 2026-07-01T10:00:00Z.
- **Implication**: The description digest was posted during the first triage run.
  It records the hash of the Vulnerability issue description at triage time. A
  second run should not post a duplicate digest comment.
- **Action**: No new digest comment needed. The existing digest comment already
  captures the description state. Posting another would be redundant (though not
  harmful, it adds noise).

### 5. Post-Triage Summary Comment

- **Detected**: Comment #2 on TC-8001 is the post-triage summary documenting:
  - Version impact: RHTPA 2.2.0 and 2.2.1 affected, RHTPA 2.2.2+ not affected
  - Affects Versions correction applied
  - ai-cve-triaged label added
  - Remediation tasks created: TC-8100 (upstream backport), TC-8101 (downstream propagation)
  - Transition to In Progress
  Posted by sdlc-workflow/triage-security on 2026-07-01T10:01:00Z.
- **Implication**: The summary comment is the final triage output artifact. Its
  presence confirms that the prior triage completed all steps through the summary.
  Posting a duplicate summary would create confusion in the audit trail.
- **Action**: No new summary comment needed. The existing summary already
  documents the complete triage outcome.

### 6. Affects Versions Already Correct

- **Detected**: The Jira `Affects Versions` field contains `RHTPA 2.2.0, RHTPA 2.2.1`.
- **Implication**: Step 3 compares PSIRT-assigned Affects Versions against the
  version impact table (scoped to the 2.2.x stream). The lock file analysis shows:
  - 2.2.0 (v0.4.5): quinn-proto 0.11.9 -- affected
  - 2.2.1 (v0.4.8): quinn-proto 0.11.12 -- affected
  - 2.2.2 (v0.4.9): retag of 2.2.1 -- affected, but 2.2.2 is not a released product
    version listed in Affects Versions (it is a build-level retag)
  - 2.2.3 (v0.4.11): quinn-proto 0.11.14 -- NOT affected
  - 2.2.4 (v0.4.12): quinn-proto 0.11.14 -- NOT affected
  The correct Affects Versions for this stream are RHTPA 2.2.0 and RHTPA 2.2.1,
  which matches what is already set.
- **Action**: No Affects Versions correction needed. The values are already correct
  from the prior triage run.

## Summary of Idempotency Checks

| Artifact | Present? | Step | Action |
|----------|----------|------|--------|
| ai-cve-triaged label | YES | Post-Triage Summary | Skip -- already applied |
| Status: In Progress | YES | Step 0.7 / Step 8 | Skip transitions -- already past target states |
| Remediation task TC-8100 (upstream backport) | YES | Step 8 Case A | Skip -- task exists with correct CVE, stream, and Depend link |
| Remediation task TC-8101 (downstream propagation) | YES | Step 8 Case A | Skip -- task exists with correct CVE, stream, and Depend link |
| Blocks link TC-8101 -> TC-8100 | YES | Step 8 linkage | Skip -- dependency ordering already established |
| Description digest comment | YES | Post-creation | Skip -- digest already recorded |
| Post-triage summary comment | YES | Post-Triage Summary | Skip -- audit trail already complete |
| Affects Versions = RHTPA 2.2.0, 2.2.1 | YES (correct) | Step 3 | Skip -- values match version impact analysis |
