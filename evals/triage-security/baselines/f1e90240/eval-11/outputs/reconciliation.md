# Step 4.4 -- Preemptive Task Reconciliation: TC-8021

## JQL Search

Query:
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

Fields requested: summary, status, labels, issuelinks

## Search Results

| Key | Summary | Status | Labels | Issue Links |
|-----|---------|--------|--------|-------------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive | Related: TC-8020 |

## Stream Filtering

- Current issue stream suffix: `[rhtpa-2.1]` -> stream name `rhtpa-2.1`
- TC-8022 summary contains `(rhtpa-2.1)` -> **matches** the current issue's stream

Result: **TC-8022 is a matching preemptive task** for CVE-2026-55123 in stream rhtpa-2.1.

## Preemptive Task Origin

TC-8022 was created during Step 8 Case B (cross-stream impact / proactive remediation) of a prior triage session on **TC-8020**, which is the CVE Jira for CVE-2026-55123 scoped to stream **rhtpa-2.2**. That triage identified that stream 2.1.x was also affected but had no stream-specific CVE Jira at the time, so it created TC-8022 as a preemptive remediation task with:

- Labels: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
- Link type: "Related" to TC-8020 (not "Depend", because TC-8020 belongs to a different stream)

## Reconciliation Actions

Per Step 4.4 of the triage-security skill, the following actions are taken when a matching preemptive task is found:

### a. Link TC-8021 to TC-8022 with "Depend"

```
jira.create_link(
  inwardIssue: TC-8021,
  outwardIssue: TC-8022,
  type: "Depend"
)
```

This establishes the standard remediation linkage between the CVE Jira (TC-8021) and its remediation task (TC-8022), identical to how a freshly-created remediation task would be linked.

### b. Remove the `security-preemptive` label from TC-8022

Current labels: `ai-generated-jira, Security, CVE-2026-55123, security-preemptive`

Updated labels: `ai-generated-jira, Security, CVE-2026-55123`

```
jira.edit_issue(TC-8022, fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed because TC-8022 is now linked to a proper CVE Jira (TC-8021) for its stream. It is no longer a preemptive task -- it is a standard remediation task.

### c. Engineer notification

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (stream rhtpa-2.2, linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

### d. Record reconciliation

Remediation for stream 2.1.x is recorded as already existing via TC-8022. Step 8 will skip task creation for this stream.

## Issue Link Summary After Reconciliation

TC-8021 (CVE Jira, stream rhtpa-2.1):
- **Depend** -> TC-8022 (remediation task, now standard)

TC-8022 (remediation task, formerly preemptive):
- **Depend** <- TC-8021 (its own CVE Jira)
- **Related** <-> TC-8020 (originating CVE Jira from stream rhtpa-2.2)

TC-8020 (CVE Jira, stream rhtpa-2.2):
- **Related** <-> TC-8022 (cross-stream remediation task)
