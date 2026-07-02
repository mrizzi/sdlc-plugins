# Triage Outcome: TC-8021 (CVE-2026-55123)

## Summary

TC-8021 is a Vulnerability issue for CVE-2026-55123 (tokio use-after-free, versions
before 1.42.0) scoped to stream rhtpa-2.1. Triage determined that a preemptive
remediation task (TC-8022) already existed for this exact CVE and stream, created
during a prior cross-stream triage of TC-8020 (stream rhtpa-2.2). The preemptive
task was reconciled into a standard remediation task -- no new tasks were created.

## How the Preemptive Task Was Reconciled

### Origin of TC-8022

When TC-8020 (the same CVE-2026-55123, scoped to stream rhtpa-2.2) was triaged
previously, Step 8 Case B (cross-stream impact) detected that stream 2.1.x was
also affected by the vulnerability but had no CVE Jira of its own. Following the
Case B procedure, TC-8022 was created as a proactive remediation task with:

- Labels: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
- Link: "Related" to TC-8020 (the originating CVE Jira)
- Summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)"

### Reconciliation During TC-8021 Triage

When PSIRT subsequently created TC-8021 as the stream-specific CVE Jira for rhtpa-2.1,
the triage of TC-8021 triggered Step 4.4 (preemptive task reconciliation). The
procedure:

1. **JQL search** for tasks with labels `security-preemptive` and `CVE-2026-55123`
   found TC-8022.

2. **Stream matching** confirmed TC-8022's summary contains `(rhtpa-2.1)`, matching
   the current issue's stream scope.

3. **Reconciliation actions** executed:
   - **Linked** TC-8021 to TC-8022 with "Depend" (standard remediation linkage),
     establishing TC-8022 as the official remediation task for TC-8021.
   - **Removed** the `security-preemptive` label from TC-8022, converting it from
     a preemptive task to a standard remediation task. Updated labels:
     `["ai-generated-jira", "Security", "CVE-2026-55123"]`.
   - **Recorded** that remediation exists for the rhtpa-2.1 stream, so Step 8
     skips new task creation.

4. **Step 8 skipped task creation** for the rhtpa-2.1 stream because reconciliation
   confirmed TC-8022 already covers the needed remediation (bumping tokio to 1.42.0).

### Final Issue Graph

```
TC-8020 (CVE Jira, stream rhtpa-2.2)
  |
  +-- "Related" --> TC-8022 (remediation task, stream rhtpa-2.1)
                      ^
TC-8021 (CVE Jira, stream rhtpa-2.1)
  |
  +-- "Depend" ---> TC-8022 (remediation task, stream rhtpa-2.1)
```

- TC-8022 retains its "Related" link to TC-8020 (documents the cross-stream origin).
- TC-8022 gains a "Depend" link from TC-8021 (standard CVE-to-remediation linkage).
- TC-8022 no longer carries the `security-preemptive` label (it is now a standard
  remediation task owned by TC-8021).

## Outcome

- **Triage result**: Affected -- remediation already exists via preemptive task
- **New tasks created**: None (TC-8022 was reconciled, not duplicated)
- **TC-8022 status**: Converted from preemptive to standard remediation task
- **Key benefit**: The preemptive reconciliation mechanism prevented creation of a
  duplicate remediation task. The work that was proactively queued during TC-8020's
  triage is seamlessly adopted by TC-8021 without losing any context or linkage
  history.
