# Step 4.4 -- Preemptive Task Reconciliation

## Context

TC-8021 is a PSIRT-created Vulnerability issue for CVE-2026-55123 (tokio use-after-free) scoped to stream rhtpa-2.1 (2.1.x). A prior triage of TC-8020 (the same CVE for stream rhtpa-2.2) identified that stream 2.1.x was also affected and created a preemptive remediation task TC-8022 under Step 7 Case B.

Now that PSIRT has created TC-8021 as the stream-specific CVE Jira for rhtpa-2.1, Step 4.4 reconciliation must link the new CVE Jira to the existing preemptive task and convert it into a standard remediation task.

## 4.4.1 -- Search for Preemptive Tasks

JQL query (simulated):

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

### Search Results

| Key | Summary | Status | Labels |
|-----|---------|--------|--------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |

**Issue links on TC-8022:**
- Related: TC-8020 (originating CVE Jira, stream rhtpa-2.2)

## 4.4.2 -- Filter to Current Stream

TC-8022's summary contains `(rhtpa-2.1)`, which matches the current issue's stream suffix `[rhtpa-2.1]`.

**Match found**: TC-8022 is a preemptive remediation task for this exact CVE and stream.

## 4.4.3 -- Reconciliation Actions (Proposed)

The following Jira mutations are proposed for engineer confirmation:

### Action 1: Link TC-8021 to TC-8022 with "Depend"

Create a standard remediation linkage between the new CVE Jira and the preemptive task:

```
jira.create_link(
  inwardIssue: "TC-8021",
  outwardIssue: "TC-8022",
  type: "Depend"
)
```

**Rationale**: TC-8022 is now the remediation task for TC-8021 (the stream-specific CVE Jira). The "Depend" link type is the standard linkage used between Vulnerability issues and their remediation Tasks.

### Action 2: Remove `security-preemptive` label from TC-8022

Update TC-8022's labels to remove the preemptive marker:

```
Current labels: ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
Updated labels: ["ai-generated-jira", "Security", "CVE-2026-55123"]

jira.edit_issue("TC-8022", fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

**Rationale**: The `security-preemptive` label indicates a proactive task created before a stream-specific CVE Jira existed. Now that TC-8021 exists, TC-8022 transitions from a preemptive task to a standard remediation task. Removing the label reflects this status change.

### Action 3: Preserve existing "Related" link to TC-8020

The existing "Related" link between TC-8022 and TC-8020 (the originating CVE from stream rhtpa-2.2) is preserved. This link provides cross-stream traceability and should not be removed.

**Link summary after reconciliation:**
- TC-8022 --[Depend]--> TC-8021 (new: stream-specific CVE Jira for rhtpa-2.1)
- TC-8022 --[Related]--> TC-8020 (existing: originating CVE Jira for rhtpa-2.2)

## 4.4.4 -- Reconciliation Record

Remediation already exists for stream 2.1.x via TC-8022. Step 7 will **skip** new remediation task creation for this stream.

**Engineer notification:**

```
Existing preemptive remediation task TC-8022 found for this CVE and stream.
Created from cross-stream analysis of TC-8020 (stream rhtpa-2.2, linked via "Related").

Proposed actions:
- Link TC-8021 --> TC-8022 with "Depend"
- Remove "security-preemptive" label from TC-8022

The preemptive task will become a standard remediation task for this CVE Jira.
Skipping new remediation task creation in Step 7.
```
