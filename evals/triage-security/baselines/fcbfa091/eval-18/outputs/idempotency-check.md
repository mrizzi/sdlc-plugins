# Idempotency Check -- Pre-existing Triage Artifacts

This document records every triage artifact detected on TC-8001 during re-run
and the corresponding skip decision. The triage-security skill is designed to
be idempotent: re-running triage on an already-triaged issue must detect all
prior artifacts and avoid duplicating any mutations.

## Summary

| # | Artifact | Detected | Action | Reason |
|---|----------|----------|--------|--------|
| 1 | `ai-cve-triaged` label | Yes | **Skip** -- do not add label | Label already present in issue labels |
| 2 | Status: In Progress | Yes | **Skip** -- do not transition | Issue already past New/Assigned status |
| 3 | Depend link to TC-8100 (upstream backport task) | Yes | **Skip** -- do not create task | Remediation task already exists and is linked |
| 4 | Depend link to TC-8101 (downstream propagation task) | Yes | **Skip** -- do not create task | Remediation task already exists and is linked |
| 5 | Description digest comment | Yes | **Skip** -- do not post digest | Digest comment already present from prior run |
| 6 | Post-triage summary comment | Yes | **Skip** -- do not post summary | Summary comment already present from prior run |

## Artifact Detection Details

### 1. Label: `ai-cve-triaged`

**Detection method**: Inspect the issue's `labels` field from the Jira response.

**Evidence**: The labels array contains `ai-cve-triaged` alongside `CVE-2026-31812`
and `pscomponent:org/rhtpa-server`.

**Skip rationale**: The Post-Triage Summary (SKILL.md) adds `ai-cve-triaged` to mark
an issue as triaged. Since the label is already present, adding it again would be a
no-op at best and risks duplicate API calls. The re-run skips the label addition.

### 2. Status: In Progress

**Detection method**: Inspect the issue's `status` field from the Jira response.

**Evidence**: Current status is `In Progress`, which is beyond both `New` and `Assigned`.

**Skip rationale**: Step 0.7 transitions the issue from New to Assigned, and the
Post-Triage Summary flow transitions it further. The issue is already in `In Progress`,
which is a later workflow state. Transitioning backward is not supported by the Jira
workflow, and transitioning forward is not within the scope of the triage skill (the
issue is actively being worked). The re-run skips the status transition. Per the
Status-aware handling section of the skill, issues in In Progress trigger a warning
that the issue may be actively worked on -- in a re-run context this is expected
because the prior triage already advanced the status.

### 3. Depend Link: TC-8100 (Upstream Backport Task)

**Detection method**: Inspect the issue's `issuelinks` field for links with type `Depend`.

**Evidence**: A Depend link exists to TC-8100 with summary "Backport quinn-proto fix
to >= 0.11.14 on release/0.4.z [rhtpa-2.2]", status In Progress, and labels
`ai-generated-jira, Security, CVE-2026-31812`. This matches the expected upstream
backport remediation task template for a Cargo ecosystem vulnerability.

**Skip rationale**: Step 8 / Case A creates remediation tasks and links them via Depend.
The upstream backport task already exists with the correct summary pattern, labels, and
link type. Creating a duplicate task would produce redundant work items. The re-run
skips remediation task creation for the upstream backport.

### 4. Depend Link: TC-8101 (Downstream Propagation Task)

**Detection method**: Inspect the issue's `issuelinks` field for links with type `Depend`.

**Evidence**: A Depend link exists to TC-8101 with summary "Propagate quinn-proto bump
to rhtpa-server release branch [rhtpa-2.2]", status Open, and labels
`ai-generated-jira, Security, CVE-2026-31812`. It also has a Blocks relationship
to TC-8100, matching the expected downstream-blocks-upstream pattern for Cargo
ecosystems.

**Skip rationale**: Step 8 / Case A creates a downstream propagation subtask blocked by
the upstream task for source dependency ecosystems. TC-8101 already exists with the
correct structure (Depend link to CVE issue, Blocks link to upstream task TC-8100).
Creating a duplicate would produce redundant work items. The re-run skips remediation
task creation for the downstream propagation.

### 5. Description Digest Comment

**Detection method**: Scan the issue's comments for the digest comment marker prefix
`[sdlc-workflow] Description digest:`.

**Evidence**: Comment #1 contains `[sdlc-workflow] Description digest:
sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2`,
posted by `sdlc-workflow/triage-security` on 2026-07-01T10:00:00Z.

**Skip rationale**: Per `shared/description-digest-protocol.md`, the digest comment
records a hash of the issue description at triage time. It is posted once per triage
run. Since a digest comment already exists from the prior run (2026-07-01), posting
another would create a duplicate comment. The description has not changed (the digest
value would be identical), so no update is needed either. The re-run skips posting
the digest comment.

### 6. Post-Triage Summary Comment

**Detection method**: Scan the issue's comments for the triage summary marker. The
summary comment contains the AI-generated footer
`This comment was AI-generated by [sdlc-workflow/triage-security]` and documents
the triage outcome including version impact, Affects Versions corrections, and
remediation task links.

**Evidence**: Comment #2 contains the full post-triage summary documenting:
- Version impact: RHTPA 2.2.0 and 2.2.1 affected, RHTPA 2.2.2+ not affected
- Affects Versions corrected to RHTPA 2.2.0, RHTPA 2.2.1
- Label `ai-cve-triaged` added
- Remediation tasks: TC-8100 (upstream backport), TC-8101 (downstream propagation)
- Transitioned to In Progress
- Posted by `sdlc-workflow/triage-security` on 2026-07-01T10:01:00Z

**Skip rationale**: The post-triage summary is the final artifact of the triage
workflow. It already captures the complete triage outcome from the prior run. Posting
a second summary would create a duplicate comment with identical content (since no
triage state has changed). The re-run skips posting the summary comment.
