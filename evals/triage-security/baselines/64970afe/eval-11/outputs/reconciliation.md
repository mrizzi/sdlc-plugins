# Step 4.4 -- Preemptive Task Reconciliation

## Context

TC-8021 is a new CVE Vulnerability issue for CVE-2026-55123 (tokio use-after-free) scoped to stream [rhtpa-2.1]. A prior triage of TC-8020 (the same CVE for stream [rhtpa-2.2]) already ran Step 8 Case B cross-stream analysis and created a preemptive remediation task TC-8022 for stream rhtpa-2.1.

## Step 4.4.1 -- Search for Preemptive Tasks

JQL query:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

Fields requested: summary, status, labels, issuelinks

### Search Results

| Key | Summary | Status | Labels |
|-----|---------|--------|--------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |

Issue links on TC-8022:
- Related: TC-8020 (originating CVE Jira, stream [rhtpa-2.2])

## Step 4.4.2 -- Filter to Current Stream

Current issue stream suffix: `[rhtpa-2.1]` (stream 2.1.x)

TC-8022 summary contains `(rhtpa-2.1)` -- **matches** the current issue's stream.

**Result**: TC-8022 is a matching preemptive remediation task for this CVE and stream.

## Step 4.4.3 -- Reconciliation Actions

A matching preemptive task was found. The following reconciliation actions are required:

### a. Link CVE Jira to preemptive task (Depend)

Create a "Depend" link from TC-8021 (the new CVE Jira) to TC-8022 (the preemptive task), establishing the standard remediation linkage:

```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

This replaces the existing "Related" link pattern (TC-8022 was previously linked to TC-8020 via "Related" as a preemptive task) with the standard "Depend" linkage to the now-existing stream-specific CVE Jira TC-8021.

### b. Remove the `security-preemptive` label

The `security-preemptive` label is removed because TC-8022 is now linked to a proper CVE Jira (TC-8021) for its stream. It is no longer preemptive -- it is a standard remediation task.

Current labels on TC-8022: `ai-generated-jira, Security, CVE-2026-55123, security-preemptive`

Updated labels (after removing `security-preemptive`): `ai-generated-jira, Security, CVE-2026-55123`

```
jira.edit_issue("TC-8022", fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

### c. Inform the engineer

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (stream [rhtpa-2.2], linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

### d. Record reconciliation

Remediation already exists for stream 2.1.x via TC-8022. Step 8 will skip task creation for this stream.

## Link Landscape After Reconciliation

```
TC-8020 (CVE Jira, stream rhtpa-2.2)
  |
  +-- Related --> TC-8022 (remediation task, stream rhtpa-2.1)
                    ^
                    |
TC-8021 (CVE Jira, stream rhtpa-2.1)
  |
  +-- Depend ---> TC-8022 (remediation task, stream rhtpa-2.1)
```

TC-8022 retains its "Related" link to TC-8020 (the originating CVE from the prior triage) and now also has a "Depend" link from TC-8021 (the stream-specific CVE Jira). The `security-preemptive` label is removed, marking the transition from preemptive to standard remediation.
