# Step 4.4 -- Preemptive Task Reconciliation

## JQL Search

Query executed:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

Fields requested: summary, status, labels, issuelinks

## Search Results

| Issue | Summary | Status | Labels |
|-------|---------|--------|--------|
| TC-8022 | Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1) | Open | ai-generated-jira, Security, CVE-2026-55123, security-preemptive |

TC-8022 has an existing "Related" link to TC-8020 (the originating CVE Jira from stream rhtpa-2.2).

## Stream Filtering

- Current issue TC-8021 stream suffix: `[rhtpa-2.1]` -> stream `rhtpa-2.1`
- TC-8022 summary contains `(rhtpa-2.1)` -> **matches** the current issue's stream
- Result: TC-8022 is a matching preemptive task for this CVE and stream

## Reconciliation Actions

Since a matching preemptive task (TC-8022) was found:

### a. Link CVE Jira to preemptive task

Create a "Depend" link (standard remediation linkage) from the new CVE Jira to the preemptive task:

```
jira.create_link(
  inwardIssue: TC-8021,
  outwardIssue: TC-8022,
  type: "Depend"
)
```

This establishes TC-8022 as the remediation task for TC-8021, using the same link type that would be used if a new remediation task were created from scratch.

### b. Remove security-preemptive label

Remove the `security-preemptive` label from TC-8022 since it is now linked to a proper CVE Jira (TC-8021):

```
current_labels = ["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]
updated_labels = ["ai-generated-jira", "Security", "CVE-2026-55123"]

jira.edit_issue(TC-8022, fields={
  "labels": ["ai-generated-jira", "Security", "CVE-2026-55123"]
})
```

The `security-preemptive` label is removed because TC-8022 is no longer a preemptive task -- it is now a standard remediation task linked to its own stream's CVE Jira.

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

Remediation already exists for stream rhtpa-2.1 via TC-8022. Step 8 will skip task creation for this stream.

## Link Topology After Reconciliation

```
TC-8020 (CVE Jira, rhtpa-2.2)
  |
  +-- Related --> TC-8022 (remediation task, rhtpa-2.1) [original link from Case B]
                    |
TC-8021 (CVE Jira, rhtpa-2.1)
  |
  +-- Depend ---> TC-8022 (remediation task, rhtpa-2.1) [new link from reconciliation]
```

TC-8022 is now linked to both:
- TC-8020 via "Related" (the originating CVE from which it was preemptively created)
- TC-8021 via "Depend" (the stream-specific CVE Jira it now serves as remediation for)
