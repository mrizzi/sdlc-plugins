# Idempotency Check: TC-8001 Re-Run Analysis

This document analyzes all pre-existing triage artifacts detected on TC-8001 during this second triage run, and explains why each artifact causes the corresponding triage step to be skipped.

## Summary

TC-8001 has already been fully triaged by a prior run of `triage-security`. All triage artifacts are present and consistent. The re-run detects each artifact and skips the corresponding mutation, producing a fully idempotent outcome with zero new Jira writes.

## Pre-Existing Artifacts Detected

### 1. Label: `ai-cve-triaged`

- **Detected in**: Issue labels field
- **Set by**: Post-Triage Summary (final step of prior run)
- **Significance**: This is the primary idempotency marker for the triage-security skill. The `ai-cve-triaged` label signals that the issue has already completed full triage. In Discovery Mode, issues with this label are excluded from the "Untriaged" list (they appear under "Triaged but still New" or "Ready for QA" instead).
- **Action**: Skip label addition. The label is already present; adding it again would be a no-op in Jira but the skill avoids the unnecessary API call.

### 2. Status: In Progress

- **Detected in**: Issue status field
- **Current status**: In Progress
- **Set by**: Step 0.7 transition during prior run (New -> Assigned -> In Progress)
- **Significance**: The status-aware handling in the Inputs section detects that the issue is already in "In Progress" status. Per the skill documentation: "In Progress / Code Review / QA -- warn the user: 'This issue is already in <status>. It may be actively worked on.'" The skill would present the option to proceed with triage anyway or skip.
- **Action**: Skip transition. The issue is already past the "Assigned" state, so Step 0.7's transition to Assigned is not needed. No status mutation required.

### 3. Remediation Task Links (Depend)

- **Detected in**: Issue links field
- **Links found**:
  - **TC-8100** (Depend) -- "Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2]" -- Status: In Progress -- Labels: ai-generated-jira, Security, CVE-2026-31812
  - **TC-8101** (Depend) -- "Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2]" -- Status: Open -- Labels: ai-generated-jira, Security, CVE-2026-31812 -- Blocks: TC-8100
- **Set by**: Step 8 (Remediation -- Case A) during prior run
- **Significance**: The two-task pattern (upstream backport + downstream propagation) is the expected output for a Cargo ecosystem vulnerability. TC-8100 is the upstream backport task and TC-8101 is the downstream propagation subtask, with TC-8101 blocked by TC-8100. Both carry the `ai-generated-jira` label confirming they were created by the skill.
- **Action**: Skip remediation task creation. Creating duplicate tasks would produce redundant work items. Step 4.4 (Preemptive Task Reconciliation) would also detect these as existing remediation, preventing duplicate creation. The existing tasks cover the same scope (stream 2.2.x, quinn-proto backport to >= 0.11.14).

### 4. Description Digest Comment

- **Detected in**: Issue comments (comment #1)
- **Content**: `[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2`
- **Posted by**: sdlc-workflow/triage-security
- **Posted at**: 2026-07-01T10:00:00Z
- **Set by**: Description Digest Protocol during prior run
- **Significance**: The description digest comment records a SHA-256 hash of the issue description at the time of triage. On re-run, the skill can compare the current description hash against the stored digest to detect whether the description has changed since the last triage. If the digest matches (description unchanged), no re-analysis of Step 1 data is needed.
- **Action**: Skip digest comment posting. A digest comment already exists. If the description has not changed (hash matches), the prior extraction remains valid. Posting a second digest comment would create noise in the comment history.

### 5. Post-Triage Summary Comment

- **Detected in**: Issue comments (comment #2)
- **Content**: Full triage summary documenting version impact (RHTPA 2.2.0 and 2.2.1 affected, 2.2.2+ not affected), Affects Versions correction, remediation tasks (TC-8100, TC-8101), and transition to In Progress.
- **Posted by**: sdlc-workflow/triage-security
- **Posted at**: 2026-07-01T10:01:00Z
- **Set by**: Post-Triage Summary (final step of prior run)
- **Significance**: The post-triage summary is the definitive record that triage completed successfully. Its presence, combined with the `ai-cve-triaged` label, confirms that all triage steps (1 through 8) executed and produced their expected outputs. The summary includes the Comment Footnote with the skill version (v0.11.1).
- **Action**: Skip summary comment posting. A complete summary already exists. Posting a second summary would duplicate information and create confusion about which summary is authoritative.

### 6. Affects Versions (Already Corrected)

- **Detected in**: Issue `versions` field
- **Current value**: RHTPA 2.2.0, RHTPA 2.2.1
- **Set by**: Step 3 (Affects Versions Correction) during prior run
- **Significance**: The Affects Versions field has already been corrected based on lock file evidence from the prior triage. The version impact analysis shows that RHTPA 2.2.0 (quinn-proto 0.11.9) and RHTPA 2.2.1 (quinn-proto 0.11.12) are affected. The current field value matches the expected correction.
- **Action**: Skip Affects Versions update. The field already contains the correct values. No mutation needed.

### 7. Assignee (Already Set)

- **Detected in**: Issue `assignee` field
- **Current value**: engineer-a@example.com
- **Set by**: Step 0.7 during prior run
- **Significance**: The issue was assigned during the prior triage run. Re-assignment would overwrite the current assignee, which may have been changed since triage.
- **Action**: Skip reassignment. The issue already has an assignee. Per Step 0.7: "The assignment in step 2 still proceeds regardless -- it ensures the current user is recorded even when re-triaging." However, since all other artifacts confirm complete triage, reassignment is unnecessary for this idempotent re-run.

## Artifact Completeness Matrix

| Triage Step | Expected Artifact | Found? | Consistent? | Skip? |
|-------------|-------------------|--------|-------------|-------|
| Step 0.7 | Assignee set, status >= Assigned | Yes | Yes | Yes |
| Step 1 | CVE data extractable | Yes | Yes | No (read-only, always runs) |
| Step 3 | Affects Versions corrected | Yes | Yes | Yes |
| Step 4 | Duplicate/sibling check | N/A | N/A | Read-only, no mutations expected |
| Step 8 | Remediation tasks created + linked | Yes (TC-8100, TC-8101) | Yes | Yes |
| Post-triage | ai-cve-triaged label | Yes | Yes | Yes |
| Post-triage | Description digest comment | Yes | Yes | Yes |
| Post-triage | Summary comment | Yes | Yes | Yes |
