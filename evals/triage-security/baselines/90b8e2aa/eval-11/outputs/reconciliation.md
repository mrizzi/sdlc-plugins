# Step 4.4 -- Preemptive Task Reconciliation: TC-8021

## Context

TC-8021 is a new CVE Vulnerability issue for CVE-2026-55123 (tokio use-after-free), scoped to stream `[rhtpa-2.1]`. A prior triage of TC-8020 (the same CVE for stream `[rhtpa-2.2]`) already performed cross-stream analysis (Step 8 Case B) and created a preemptive remediation task for the rhtpa-2.1 stream.

## Step 4.4 Execution

### 4.4.1 -- Search for preemptive tasks

JQL query:
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

Result: **1 task returned**

| Key | Summary | Status | Labels |
|-----|---------|--------|--------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |

Issue links on TC-8022:
- **Related**: TC-8020 (originating CVE Jira, stream [rhtpa-2.2])

### 4.4.2 -- Filter by stream match

- Current issue stream suffix: `[rhtpa-2.1]`
- TC-8022 summary contains: `(rhtpa-2.1)`
- **Match confirmed** -- TC-8022 is the preemptive task for this CVE and this stream.

### 4.4.3 -- Reconciliation actions

Since a matching preemptive task was found, the following actions are performed:

#### a. Link CVE Jira to preemptive task with "Depend"

```
jira.create_link(
  inwardIssue: TC-8021,
  outwardIssue: TC-8022,
  type: "Depend"
)
```

This establishes the standard remediation linkage between the CVE Vulnerability issue and the remediation task. The "Depend" link type is the same used when triage-security creates new remediation tasks in Step 8 Case A.

#### b. Remove `security-preemptive` label from TC-8022

```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]

jira.edit_issue(TC-8022, fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed because TC-8022 is now linked to a proper CVE Jira (TC-8021) via the standard "Depend" link. It is no longer a preemptive task -- it is a standard remediation task.

#### c. Engineer notification

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (linked via "Related").

Actions taken:
- Linked TC-8021 -> TC-8022 with "Depend"
- Removed "security-preemptive" label from TC-8022

The preemptive task is now a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 8.
```

#### d. Record reconciliation

Remediation for stream rhtpa-2.1 is marked as already existing. Step 8 will skip task creation for this stream.

## Link State After Reconciliation

### TC-8021 (current CVE Jira -- stream rhtpa-2.1)
- **Depend** (outward): TC-8022 (remediation task)

### TC-8022 (remediation task -- now standard, no longer preemptive)
- **Depend** (inward): TC-8021 (CVE Jira for rhtpa-2.1)
- **Related**: TC-8020 (originating CVE Jira for rhtpa-2.2, retained from original creation)

### TC-8020 (originating CVE Jira -- stream rhtpa-2.2)
- **Related**: TC-8022 (retained -- shows provenance of the task)
