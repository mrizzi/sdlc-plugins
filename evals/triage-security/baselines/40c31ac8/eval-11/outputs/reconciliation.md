# Step 4.4 -- Preemptive Task Reconciliation: TC-8021

## Context

When triaging TC-8021 (CVE-2026-55123, stream rhtpa-2.1), Step 4.4 checks whether a
proactive remediation task already exists for this CVE and stream. Such tasks are created
by Step 8 Case B during cross-stream triage of a sibling CVE Jira on a different stream.

## JQL Search

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

Fields requested: summary, status, labels, issuelinks

## Search Results

One matching task found:

| Field | Value |
|-------|-------|
| Key | TC-8022 |
| Summary | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) |
| Status | Open |
| Labels | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |
| Issue Links | Related: TC-8020 (originating CVE Jira, stream rhtpa-2.2) |

## Stream Matching

- Current issue stream: rhtpa-2.1 (from summary suffix `[rhtpa-2.1]`)
- TC-8022 summary contains: `(rhtpa-2.1)` -- **matches the current issue's stream**

TC-8022 is a preemptive remediation task created for the rhtpa-2.1 stream during a prior
cross-stream triage of TC-8020 (which is scoped to stream rhtpa-2.2). The preemptive
task was created because TC-8020's triage (Step 8 Case B) detected that stream 2.1.x was
also affected but had no CVE Jira of its own at that time.

## Reconciliation Actions

Per the Step 4.4 procedure, the following actions are required:

### 4.4.3a -- Link the new CVE Jira to the preemptive task

Create a "Depend" link (standard remediation linkage) from TC-8021 to TC-8022:

```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

This replaces the existing "Related" link between TC-8022 and TC-8020 with a proper
"Depend" link to the stream-specific CVE Jira (TC-8021). The "Related" link to TC-8020
remains intact -- it documents the originating cross-stream triage.

### 4.4.3b -- Remove the security-preemptive label

Update TC-8022's labels to remove `security-preemptive`, converting it from a
preemptive task to a standard remediation task:

```
Current labels:  ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
Updated labels:  ["ai-generated-jira", "Security", "CVE-2026-55123"]

jira.edit_issue("TC-8022", fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

### 4.4.3c -- Inform the engineer

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

### 4.4.3d -- Record the reconciliation

Mark that remediation already exists for the rhtpa-2.1 stream so that Step 8
skips task creation for this stream. No new upstream backport task or downstream
propagation subtask needs to be created.

## Post-Reconciliation State

| Entity | Before Reconciliation | After Reconciliation |
|--------|----------------------|---------------------|
| TC-8021 (CVE Jira) | No links to remediation tasks | Linked to TC-8022 via "Depend" |
| TC-8022 (remediation task) | Labels include `security-preemptive`; linked to TC-8020 via "Related" only | `security-preemptive` label removed; linked to TC-8021 via "Depend" and TC-8020 via "Related" |
| Step 8 | Would create new remediation tasks for rhtpa-2.1 | Skips task creation for rhtpa-2.1 (already covered by TC-8022) |
