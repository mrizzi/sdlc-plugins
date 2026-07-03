# Step 4.4 -- Preemptive Task Reconciliation: TC-8021

## JQL Search

Query executed:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

Fields requested: summary, status, labels, issuelinks

## Search Results

One preemptive task found:

| Field | Value |
|-------|-------|
| Key | TC-8022 |
| Summary | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) |
| Status | Open |
| Labels | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |
| Issue Links | Related: TC-8020 (originating CVE Jira, stream [rhtpa-2.2]) |

## Stream Matching

- Current issue stream suffix: `[rhtpa-2.1]` (stream 2.1.x)
- TC-8022 summary contains `(rhtpa-2.1)` -- **matches** the current issue's stream

TC-8022 is a preemptive remediation task created during the prior triage of TC-8020 (stream [rhtpa-2.2]). When TC-8020 was triaged, the cross-stream impact analysis (Step 8, Case B) identified that stream 2.1.x was also affected by CVE-2026-55123 but did not yet have its own CVE Jira. TC-8022 was created as a proactive remediation task with the `security-preemptive` label and linked via "Related" to TC-8020.

## Reconciliation Actions

Per Step 4.4 of the triage-security skill, the following reconciliation actions apply:

### a. Link the new CVE Jira to the preemptive task

```
jira.create_link(
  inwardIssue: TC-8021,
  outwardIssue: TC-8022,
  type: "Depend"
)
```

This establishes the standard remediation linkage between the CVE Vulnerability issue (TC-8021) and the remediation task (TC-8022), identical to what would have been created if triage had produced the task fresh.

### b. Remove the `security-preemptive` label

```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]

jira.edit_issue(TC-8022, fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed because TC-8022 is now linked to a proper CVE Jira (TC-8021) via the "Depend" link type. It is no longer a preemptive task -- it is a standard remediation task.

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

Remediation for stream 2.1.x is recorded as already existing via the reconciled preemptive task TC-8022. Step 8 will skip task creation for this stream.

## Link Topology After Reconciliation

```
TC-8020 (CVE Jira, stream rhtpa-2.2)
  |
  +-- Related --> TC-8022 (remediation task, rhtpa-2.1)
                    |
TC-8021 (CVE Jira, stream rhtpa-2.1)
  |
  +-- Depend --> TC-8022 (remediation task, rhtpa-2.1)
```

TC-8022 is now linked to both CVE Jiras:
- **Related** to TC-8020: the originating CVE from whose cross-stream analysis TC-8022 was created
- **Depend** from TC-8021: the stream-specific CVE that TC-8022 now formally remediates
