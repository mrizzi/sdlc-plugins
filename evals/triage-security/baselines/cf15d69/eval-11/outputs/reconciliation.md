# Step 4.4 -- Preemptive Task Reconciliation Analysis

## Context

TC-8021 is a new CVE Jira for CVE-2026-55123 (tokio use-after-free) scoped to stream `rhtpa-2.1` (suffix `[rhtpa-2.1]`). A prior triage of TC-8020 (the same CVE for stream `rhtpa-2.2`) had already performed Step 7 Case B cross-stream analysis and created a preemptive remediation task for stream rhtpa-2.1.

## Step 4.4 JQL Search

The following JQL query was executed to find preemptive tasks:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

### Search Results

| Task Key | Summary | Status | Labels |
|----------|---------|--------|--------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |

### Existing Issue Links on TC-8022

- **Related**: TC-8020 (originating CVE Jira, stream `[rhtpa-2.2]`)

## Stream Matching

- Current issue stream: `rhtpa-2.1` (from TC-8021 summary suffix)
- TC-8022 summary contains: `(rhtpa-2.1)` -- **match confirmed**

The preemptive task TC-8022 was created specifically for the rhtpa-2.1 stream during cross-stream analysis of TC-8020 (the rhtpa-2.2 CVE Jira). This is exactly the scenario Step 4.4 is designed to handle.

## Reconciliation Actions

Per the Step 4.4 procedure, three actions are taken when a matching preemptive task is found:

### Action 1: Link the new CVE Jira to the preemptive task

Create a "Depend" link (standard remediation linkage) between the CVE Jira and the preemptive task:

```
jira.create_link(
  inwardIssue: TC-8021,
  outwardIssue: TC-8022,
  type: "Depend"
)
```

This establishes the standard remediation relationship: TC-8021 (Vulnerability) depends on TC-8022 (remediation Task) for resolution.

### Action 2: Remove the `security-preemptive` label

The `security-preemptive` label is removed from TC-8022 because it is now linked to a proper CVE Jira for its stream:

```
Current labels: [ai-generated-jira, Security, CVE-2026-55123, security-preemptive]
Updated labels: [ai-generated-jira, Security, CVE-2026-55123]

jira.edit_issue(TC-8022, fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The task transitions from a preemptive task to a standard remediation task.

### Action 3: Record reconciliation outcome

Remediation already exists for stream rhtpa-2.1 via TC-8022. This is recorded so that Step 7 skips new remediation task creation for this stream.

## Post-Reconciliation State

After reconciliation:

| Entity | Before | After |
|--------|--------|-------|
| TC-8021 (CVE Jira) | No links | Linked to TC-8022 via "Depend" |
| TC-8022 (remediation Task) | Labels include `security-preemptive`; linked to TC-8020 via "Related" | `security-preemptive` label removed; retains "Related" link to TC-8020; new "Depend" link from TC-8021 |

### Link Graph After Reconciliation

```
TC-8020 (CVE, rhtpa-2.2) --[Related]--> TC-8022 (Task, rhtpa-2.1)
TC-8021 (CVE, rhtpa-2.1) --[Depend]---> TC-8022 (Task, rhtpa-2.1)
```

TC-8022 now has:
- A **"Related"** link to TC-8020 (the originating CVE Jira from a different stream that triggered preemptive creation)
- A **"Depend"** link from TC-8021 (the proper CVE Jira for this stream, establishing standard remediation tracking)

## Engineer Notification

The following message would be presented to the engineer:

> Existing preemptive remediation task TC-8022 found for this CVE and stream.
> Created from cross-stream analysis of TC-8020 (stream rhtpa-2.2, linked via "Related").
>
> Actions taken:
> - Linked TC-8021 -> TC-8022 with "Depend"
> - Removed "security-preemptive" label from TC-8022
>
> The preemptive task is now a standard remediation task for this CVE Jira.
> Skipping new remediation task creation in Step 7.
