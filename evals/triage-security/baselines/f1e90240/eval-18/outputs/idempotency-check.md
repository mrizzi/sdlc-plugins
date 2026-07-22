# Idempotency Check -- Re-Run Analysis for TC-8001

This document analyzes every pre-existing triage artifact detected on TC-8001 during the second invocation of `/sdlc-workflow:triage-security`, and documents which mutations were skipped as a result.

## Summary

All triage artifacts from the prior run are present and intact. The re-run detects each one and skips the corresponding mutation. No new Jira mutations are produced.

---

## Artifact 1: `ai-cve-triaged` Label

- **Detection**: The issue's labels array includes `ai-cve-triaged`.
- **Skill behavior**: The Post-Triage Summary (end of Step 8) adds this label to mark triage as complete. On re-run, the label is already present.
- **Action**: **Skipped** -- no label mutation needed. The label is already on the issue.
- **Discovery mode impact**: If the skill were invoked without an issue key, the discovery JQL (`labels NOT IN (ai-cve-triaged)`) would exclude TC-8001 from the untriaged list entirely.

## Artifact 2: Status "In Progress"

- **Detection**: Issue status is `In Progress`, not `New` or `Assigned`.
- **Skill behavior (Step 0.7)**: The skill attempts to transition the issue to `Assigned` status, but only if the issue is in `New` status. Since `In Progress` is a later status than `Assigned`, the transition is skipped silently per the rule: "If the issue is already in Assigned or any later status, skip the transition silently."
- **Skill behavior (Status-aware handling)**: The skill detects that the issue is in `In Progress` and would present a warning: "This issue is already in In Progress. It may be actively worked on." The user is asked whether to proceed with triage anyway or skip.
- **Action**: **Skipped** -- no status transition. Assignment update may still proceed (to record the current user), but the status is not changed.

## Artifact 3: Remediation Tasks Linked via "Depend"

- **Detection**: The issue's `issuelinks` array contains two Depend links:
  - TC-8100 (upstream backport task) -- Status: In Progress
  - TC-8101 (downstream propagation subtask) -- Status: Open, blocked by TC-8100
- **Skill behavior (Step 8)**: When Case A (affected versions exist) would create remediation tasks, the skill checks existing issue links. The two expected remediation tasks (one upstream backport, one downstream propagation) already exist and are linked with the correct link type ("Depend").
- **Verification**: The existing tasks match the expected pattern:
  - TC-8100 summary matches the upstream backport template: "Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2]"
  - TC-8101 summary matches the downstream propagation template: "Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2]"
  - Both carry the expected labels: `ai-generated-jira`, `Security`, `CVE-2026-31812`
  - TC-8101 has a Blocks link to TC-8100 (correct upstream-before-downstream ordering)
- **Action**: **Skipped** -- no new tasks created, no new links created. The existing remediation tasks and their linkage are sufficient.

## Artifact 4: Description Digest Comment

- **Detection**: Comment 1 on the issue is a description digest comment:
  ```
  [sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2
  ```
  Posted by `sdlc-workflow/triage-security` on 2026-07-01T10:00:00Z.
- **Skill behavior**: The description digest protocol (shared/description-digest-protocol.md) checks for an existing digest comment before posting a new one. The existing comment matches the expected format (`[sdlc-workflow] Description digest: sha256-md:<hex>`).
- **Digest validation**: The re-run would recompute the SHA-256 digest of the current description. If the description has not changed since the first run, the digest matches and no update is needed. If the description changed, a new digest comment would be posted (this is the one case where a mutation could occur -- but the description has not changed).
- **Action**: **Skipped** -- existing digest comment is valid and current.

## Artifact 5: Post-Triage Summary Comment

- **Detection**: Comment 2 on the issue is the post-triage summary comment, documenting:
  - Version impact: RHTPA 2.2.0 and 2.2.1 affected, 2.2.2+ not affected
  - Actions taken: Affects Versions corrected, `ai-cve-triaged` label added, remediation tasks TC-8100 and TC-8101 created, transitioned to In Progress
  - Posted by `sdlc-workflow/triage-security` on 2026-07-01T10:01:00Z
- **Skill behavior**: The Post-Triage Summary is the final step. When all prior artifacts are detected as present and correct, a second summary comment would be redundant.
- **Action**: **Skipped** -- a post-triage summary already exists documenting the same triage outcome.

## Artifact 6: Affects Versions Already Correct

- **Detection**: The issue's Affects Versions field contains `RHTPA 2.2.0, RHTPA 2.2.1`.
- **Skill behavior (Step 3)**: The version impact table for stream 2.2.x shows:
  - RHTPA 2.2.0: affected (quinn-proto 0.11.9 < 0.11.14)
  - RHTPA 2.2.1: affected (quinn-proto 0.11.12 < 0.11.14)
  - RHTPA 2.2.2: affected (retag of 2.2.1), but 2.2.2 was a retag and may not have its own Jira version
  - RHTPA 2.2.3: NOT affected (quinn-proto 0.11.14)
  - RHTPA 2.2.4: NOT affected (quinn-proto 0.11.14)
  The current Affects Versions `[RHTPA 2.2.0, RHTPA 2.2.1]` matches the expected set of affected versions.
- **Action**: **Skipped** -- "Affects Versions are already correct: note this and proceed without changes."

## Artifact 7: Assignee Already Set

- **Detection**: The issue's assignee is `engineer-a@example.com`.
- **Skill behavior (Step 0.7)**: The skill assigns the issue to the current user. On re-run, the assignment update may still proceed (to update to the current user if different), but this is a safe idempotent operation -- assigning an already-assigned issue produces no visible change if the user is the same.
- **Action**: **No-op or safe overwrite** -- assignment is idempotent.

---

## Step-by-Step Re-Run Trace

| Step | Action | Outcome on Re-Run |
|------|--------|-------------------|
| 0 | Validate Configuration | Pass -- same config |
| 0.3 | Matrix Staleness Check | Timestamp 2026-06-28 is 24 days old (> 14 day threshold) -- would warn about staleness |
| 0.5 | Jira Access | Same initialization |
| 0.7 | Assign and Transition | Assign proceeds (idempotent); transition to Assigned skipped (already In Progress) |
| 1 | Data Extraction | Same parsed data (see data-extraction.md) |
| 1.5 | External CVE Enrichment | Same external data |
| 1.7 | Embargo Check | No Embargo policy URL configured -- skipped |
| 2 | Version Impact Analysis | Same version impact table |
| 3 | Affects Versions Correction | Already correct -- no mutation |
| 4 | Duplicate/Sibling Check | Existing links detected -- no new links created |
| 4.4 | Preemptive Task Reconciliation | No preemptive tasks found (existing tasks are standard, not preemptive) |
| 5 | Version Lifecycle Check | Same lifecycle status |
| 6 | Already Fixed Check | No resolved siblings -- proceed |
| 7 | Concurrent Triage Detection | No Upstream Affected Component field in Security Config -- skipped |
| 8 | Remediation | Existing remediation tasks TC-8100 and TC-8101 already linked -- no new tasks |
| Post | ai-cve-triaged label | Already present -- no mutation |
| Post | Summary comment | Already exists -- no new comment |
