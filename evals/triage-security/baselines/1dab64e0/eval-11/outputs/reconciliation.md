# Step 4.4 -- Preemptive Task Reconciliation: TC-8021

## Context

TC-8021 is a Vulnerability issue for CVE-2026-55123 (tokio use-after-free) scoped to stream `[rhtpa-2.1]`. A prior triage of TC-8020 (which covers the same CVE for stream `[rhtpa-2.2]`) already performed cross-stream impact analysis (Step 8 Case B) and created a preemptive remediation task TC-8022 for the 2.1.x stream.

## Step 4.4 Procedure

### 4.4.1 -- Search for preemptive tasks

JQL query executed:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

Result: **TC-8022** returned.

- **TC-8022** -- Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)
  - Status: Open
  - Labels: ai-generated-jira, Security, CVE-2026-55123, security-preemptive
  - Issue Links: Related to TC-8020 (originating CVE Jira, stream [rhtpa-2.2])

### 4.4.2 -- Filter to current stream

TC-8022's summary contains `(rhtpa-2.1)`, which matches the current issue's stream scope `[rhtpa-2.1]` (stream 2.1.x).

**Match confirmed**: TC-8022 is a preemptive remediation task for this CVE and this stream.

### 4.4.3 -- Reconciliation actions

Since a matching preemptive task was found, the following actions are performed:

#### a. Link the new CVE Jira to the preemptive task (Depend)

```
jira.create_link(
  inwardIssue: TC-8021,
  outwardIssue: TC-8022,
  type: "Depend"
)
```

This establishes TC-8022 as a standard remediation task for TC-8021, using the same "Depend" link type used for all remediation task linkage.

#### b. Remove the `security-preemptive` label from TC-8022

Current labels on TC-8022: `[ai-generated-jira, Security, CVE-2026-55123, security-preemptive]`

Updated labels (after filtering out `security-preemptive`): `[ai-generated-jira, Security, CVE-2026-55123]`

```
jira.edit_issue(TC-8022, fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed because TC-8022 is now linked to a proper CVE Jira (TC-8021) for its stream. It is no longer a preemptive task -- it is a standard remediation task.

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

Remediation for stream 2.1.x is recorded as already existing (via TC-8022). Step 8 will skip task creation for this stream.

## Link State After Reconciliation

TC-8022 now has the following links:
- **Related**: TC-8020 (originating CVE Jira from stream [rhtpa-2.2] -- existing link from original preemptive creation)
- **Depend**: TC-8021 (new CVE Jira for stream [rhtpa-2.1] -- link created by this reconciliation)

TC-8021 now has the following links:
- **Depend**: TC-8022 (remediation task -- standard remediation linkage)

## Why Reconciliation Matters

Without Step 4.4, the triage of TC-8021 would reach Step 8 and create a new remediation task for stream 2.1.x -- duplicating TC-8022. The reconciliation step detects the existing preemptive task, promotes it to a standard remediation task by linking it to the new CVE Jira and removing the preemptive label, and prevents duplicate task creation.
