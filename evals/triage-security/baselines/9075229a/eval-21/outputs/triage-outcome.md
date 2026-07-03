# Triage Outcome for TC-8020

## Summary

**Issue**: TC-8020 -- CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**CVE**: CVE-2026-31812
**Library**: quinn-proto
**Fix threshold**: >= 0.11.14
**Stream scope**: 2.2.x
**Ecosystem**: Cargo (source dependency)

## Triage Decision: Case A + Case B (Affected with Cross-Stream Impact)

### Case A -- Affected (within scoped 2.2.x stream)

Three versions in the 2.2.x stream ship a vulnerable version of quinn-proto:

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| RHTPA 2.2.0 | 0.11.9 | YES |
| RHTPA 2.2.1 | 0.11.12 | YES |
| RHTPA 2.2.2 | 0.11.12 (retag of 2.2.1) | YES |
| RHTPA 2.2.3 | 0.11.14 | NO |
| RHTPA 2.2.4 | 0.11.14 | NO |

Since supported versions are affected (2.2.0, 2.2.1, 2.2.2), remediation tasks are required.

#### Remediation Tasks (pending Step 7 resolution)

Because quinn-proto is a **Cargo** (source dependency) ecosystem package, two tasks would be created:

1. **Upstream backport task**: Backport the quinn-proto fix (bump to >= 0.11.14) in the source repository (rhtpa-backend) on the `release/0.4.z` branch. References upstream fix PR quinn-rs/quinn#2048.

2. **Downstream propagation subtask**: After the upstream backport lands, update the Konflux release repo (rhtpa-release.0.4.z) to reference the new source commit that includes the fix. This subtask is blocked by the upstream task.

Both tasks would be linked to TC-8020 with a "Depend" link type and follow the task-description-template.md format for /implement-task consumption.

### Case B -- Cross-Stream Impact (2.1.x also affected)

The version impact analysis reveals that the **2.1.x stream** (outside this issue's scope) is also affected:

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| RHTPA 2.1.0 | 0.11.9 | YES |
| RHTPA 2.1.1 | 0.11.9 | YES |

All 2.1.x versions ship quinn-proto 0.11.9, which is below the 0.11.14 fix threshold.

**Cross-stream impact actions:**
- Post a cross-stream impact comment on TC-8020:
  "Cross-stream impact: quinn-proto versions before 0.11.14 also affects stream 2.1.x based on lock file analysis. This stream is tracked by a companion issue (see Related links) or may require separate PSIRT triage."
- Check for existing sibling CVE Jiras for CVE-2026-31812 with stream suffix `[rhtpa-2.1]`
- If no sibling exists for 2.1.x: create preemptive remediation tasks with `security-preemptive` label and "Related" link type to TC-8020
- If a sibling exists for 2.1.x: skip preemptive task creation for that stream (it will be triaged through its own CVE issue)

## Affects Versions Correction (Step 3)

- **Current (PSIRT-assigned)**: RHTPA 2.0.0
- **Proposed correction**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Rationale**: RHTPA 2.0.0 does not match any configured version stream. Lock file analysis shows versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto < 0.11.14 (the fix threshold). Versions 2.2.3 and 2.2.4 already ship 0.11.14 and are not affected. Correction is scoped to the 2.2.x stream per the issue's `[rhtpa-2.2]` suffix.

## Step 7 -- Concurrent Triage Blocker

Remediation task creation (Step 8) is **blocked** by a concurrent triage detection:

- **TC-8019** is In Progress, assigned to engineer-b@example.com, and affects the same upstream component (quinn-proto via customfield_10632)
- The engineer must choose one of three options before remediation tasks can be created:
  1. **Wait** -- pause until TC-8019's triage completes, then re-run Step 4.3 to detect overlap
  2. **Skip** -- skip task creation and add a comment explaining the skip
  3. **Proceed** -- create tasks with a `concurrent-triage-overlap` label for cross-triage reconciliation

Until the engineer resolves this blocker, the triage analysis is complete but no remediation tasks or Jira mutations (beyond the Affects Versions correction) should be executed.

## Post-Triage Actions (after Step 7 resolution)

Once the concurrent triage situation is resolved and remediation tasks are created:

1. Add the `ai-cve-triaged` label to TC-8020
2. Post a summary comment on TC-8020 including:
   - Version impact table (both 2.2.x scoped and 2.1.x cross-stream)
   - Affects Versions correction: RHTPA 2.0.0 changed to RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
   - Triage outcome: Case A (remediation tasks created) + Case B (cross-stream impact on 2.1.x)
   - Links to all created remediation tasks
   - @mention of the issue reporter (PSIRT analyst)
   - Comment Footnote per shared/comment-footnote.md (skill: triage-security)
