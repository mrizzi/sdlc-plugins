# Step 4.4 -- Preemptive Task Reconciliation: TC-8021

## JQL Search

Search for preemptive tasks matching CVE-2026-55123:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

Fields requested: summary, status, labels, issuelinks

## Search Results

The JQL search returned **1 result**:

| Key | Summary | Status | Labels |
|-----|---------|--------|--------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |

### Issue Links on TC-8022

- **Related**: TC-8020 (originating CVE Jira, stream [rhtpa-2.2])

## Stream Filtering

- Current issue TC-8021 stream suffix: `[rhtpa-2.1]` --> stream `rhtpa-2.1`
- TC-8022 summary contains `(rhtpa-2.1)` --> **matches current stream**
- Result: TC-8022 is a valid preemptive task for this CVE and stream.

## Reconciliation Actions

Since a matching preemptive task (TC-8022) was found for CVE-2026-55123 in stream rhtpa-2.1:

### Action 1: Link TC-8021 to TC-8022 with "Depend"

```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

This establishes the standard remediation linkage between the CVE Jira and the remediation task, replacing the "Related" link that connected TC-8022 to its originating CVE Jira TC-8020.

### Action 2: Remove `security-preemptive` label from TC-8022

Current labels on TC-8022: `ai-generated-jira, Security, CVE-2026-55123, security-preemptive`

Updated labels (removing `security-preemptive`):

```
jira.edit_issue("TC-8022", fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed because TC-8022 is now linked to a proper CVE Jira (TC-8021) for its stream. It is no longer a preemptive task -- it is a standard remediation task.

### Action 3: Record reconciliation

Reconciliation recorded: remediation already exists for stream rhtpa-2.1 via TC-8022. Step 7 will **skip** remediation task creation for this stream.

## Engineer Notification

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (stream [rhtpa-2.2]),
linked via "Related".

Actions taken:
- Linked TC-8021 --> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 7.
```

## Origin of TC-8022

TC-8022 was created during a prior triage of TC-8020 (CVE-2026-55123 for stream [rhtpa-2.2]). During that triage, Step 7 Case B (cross-stream impact) identified that stream rhtpa-2.1 was also affected but had no CVE Jira of its own. A preemptive remediation task (TC-8022) was created with the `security-preemptive` label and linked via "Related" to TC-8020.

Now that PSIRT has created TC-8021 as the dedicated CVE Jira for stream [rhtpa-2.1], Step 4.4 reconciles the preemptive task by:
1. Linking it to the proper CVE Jira (TC-8021) with "Depend"
2. Removing the `security-preemptive` label
3. Preventing Step 7 from creating a duplicate remediation task
