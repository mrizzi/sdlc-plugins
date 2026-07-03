# Step 4.4 -- Preemptive Task Reconciliation: TC-8021

## Reconciliation Search

Per Step 4.4 of the triage-security skill, a JQL search was performed for preemptive
remediation tasks matching the current CVE:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

**Result**: 1 matching task found.

## Matching Preemptive Task

| Field | Value |
|-------|-------|
| Key | TC-8022 |
| Summary | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) |
| Status | Open |
| Labels | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |
| Issue Links | Related: TC-8020 (originating CVE Jira, stream rhtpa-2.2) |

## Stream Filter Validation

The preemptive task summary contains `(rhtpa-2.1)`, which matches the current issue's
stream scope (`rhtpa-2.1` from suffix `[rhtpa-2.1]`). The task passes the stream filter.

## Reconciliation Actions (Step 4.4.3)

A matching preemptive task (TC-8022) was found for CVE-2026-55123 and stream rhtpa-2.1.
The following reconciliation actions are specified by the procedure:

### a. Link the new CVE Jira to the preemptive task

Create a "Depend" link (standard remediation linkage) from the current CVE Jira to the
preemptive task:

```
jira.create_link(
  inwardIssue: TC-8021,
  outwardIssue: TC-8022,
  type: "Depend"
)
```

This establishes the standard remediation dependency: TC-8021 depends on TC-8022 for its
fix, identical to links created when triage-security creates new remediation tasks.

### b. Remove the `security-preemptive` label

The `security-preemptive` label is removed because the task is now linked to a proper
CVE Jira (TC-8021) for this stream. It is no longer preemptive -- it is a standard
remediation task.

```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]

jira.edit_issue(TC-8022, fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

### c. Engineer notification

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

### d. Record reconciliation

Remediation for the 2.1.x stream is recorded as already existing. Step 8 will skip
task creation for this stream because the preemptive task TC-8022 has been reconciled
as the standard remediation task.

## Origin Traceability

The preemptive task TC-8022 was originally created during triage of TC-8020
(CVE-2026-55123 for stream rhtpa-2.2). During that triage, Step 8 Case B identified
that stream 2.1.x was also affected but had no CVE Jira of its own. A preemptive
remediation task was created with:

- The `security-preemptive` label to mark it as proactive
- A "Related" link to TC-8020 (the originating CVE Jira)
- The CVE-2026-55123 label for searchability

Now that PSIRT has created TC-8021 as the stream-specific CVE Jira for rhtpa-2.1,
Step 4.4 reconciliation converts the preemptive task into a standard remediation task
by linking it to TC-8021 and removing the preemptive label.
