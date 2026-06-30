# Step 4.4 -- Preemptive Task Reconciliation for TC-8021

## Context

TC-8021 is a CVE Jira for CVE-2026-55123 (tokio use-after-free) scoped to stream `[rhtpa-2.1]`. A prior triage of TC-8020 (the same CVE but scoped to stream `[rhtpa-2.2]`) identified via cross-stream impact analysis (Step 7, Case B) that stream 2.1.x was also affected. At that time, no CVE Jira existed for stream 2.1.x, so a preemptive remediation task TC-8022 was created with the `security-preemptive` label.

Now that PSIRT has created TC-8021 as the dedicated CVE Jira for stream 2.1.x, Step 4.4 reconciles the existing preemptive task with this new CVE Jira.

## Step 4.4 Procedure

### 1. Search for preemptive tasks

JQL query:
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

Result: **TC-8022** -- "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)"

### 2. Filter to current stream

TC-8022 summary contains `(rhtpa-2.1)` which matches the current issue's stream suffix `[rhtpa-2.1]`. This is a matching preemptive task for this stream.

### 3. Preemptive task details

| Field | Value |
|-------|-------|
| Key | TC-8022 |
| Summary | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) |
| Status | Open |
| Labels | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |
| Issue Links | Related: TC-8020 (originating CVE Jira, stream [rhtpa-2.2]) |

### 4. Reconciliation actions

Since a matching preemptive task (TC-8022) was found for CVE-2026-55123 and stream rhtpa-2.1:

**a. Link the new CVE Jira to the preemptive task with "Depend":**

```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

This establishes the standard remediation linkage between the CVE Jira (TC-8021) and the remediation task (TC-8022), identical to the linkage that would have been created in Step 7 if the task were being created fresh.

**b. Remove the `security-preemptive` label from TC-8022:**

```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]

jira.edit_issue("TC-8022", fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed because the task is now linked to a proper CVE Jira (TC-8021). The task transitions from being a preemptive/proactive task to a standard remediation task.

**c. Engineer notification:**

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (stream [rhtpa-2.2]),
linked via "Related".

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 7.
```

**d. Record reconciliation:**

Remediation already exists for stream 2.1.x via TC-8022. Step 7 will skip task creation for this stream.

## Resulting link topology after reconciliation

```
TC-8020 (CVE Jira, stream rhtpa-2.2)
  |
  |-- Related --> TC-8022 (remediation task, rhtpa-2.1)
                     ^
                     |
TC-8021 (CVE Jira, stream rhtpa-2.1)
  |
  |-- Depend --> TC-8022 (remediation task, rhtpa-2.1)
```

TC-8022 now has two links:
1. **Related** to TC-8020 (the originating CVE that triggered the preemptive creation) -- this link remains unchanged
2. **Depend** from TC-8021 (the stream-specific CVE Jira that now owns this task) -- newly created by reconciliation

## Key observations

- The preemptive task TC-8022 already contains the correct remediation (bump tokio to 1.42.0) because it was created from the same CVE's cross-stream analysis.
- The "Related" link to TC-8020 is preserved, maintaining the audit trail of how the task was originally created.
- The new "Depend" link to TC-8021 establishes the standard parent-child relationship used by `/implement-task` and the post-triage summary.
- No duplicate remediation task is created -- the existing preemptive task is reused.
