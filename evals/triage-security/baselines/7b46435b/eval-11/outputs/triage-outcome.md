# Triage Outcome: TC-8021

## Summary

CVE-2026-55123 (tokio use-after-free, versions before 1.42.0) was triaged for stream rhtpa-2.1. An existing preemptive remediation task (TC-8022) was found and reconciled, eliminating the need to create new remediation tasks.

## How the Preemptive Task Was Reconciled

### Background

TC-8020 was the first CVE Jira created for CVE-2026-55123, scoped to stream [rhtpa-2.2]. During its triage, the cross-stream impact analysis (Step 8, Case B) determined that stream 2.1.x was also affected by the vulnerability but did not yet have its own CVE Jira. Following the Case B procedure, a preemptive remediation task (TC-8022) was created for stream rhtpa-2.1 with:

- The `security-preemptive` label to identify it as proactively created
- A "Related" link to TC-8020 (the originating CVE Jira)
- Summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)"

### Reconciliation (Step 4.4)

When TC-8021 arrived as the stream-specific CVE Jira for rhtpa-2.1, Step 4.4 searched for preemptive tasks matching CVE-2026-55123 via JQL:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123' ORDER BY created DESC
```

This returned TC-8022, whose summary contains `(rhtpa-2.1)` matching the current issue's stream. The reconciliation procedure:

1. **Created a "Depend" link** from TC-8021 to TC-8022 -- establishing the standard remediation linkage between the CVE Jira and its remediation task
2. **Removed the `security-preemptive` label** from TC-8022 -- the task is no longer preemptive because it is now linked to a proper CVE Jira
3. **Recorded the reconciliation** -- Step 8 skips new task creation for stream 2.1.x since TC-8022 already covers the remediation

### Effect on Step 8

Because the reconciliation in Step 4.4 identified TC-8022 as the existing remediation task for this stream, Step 8 (Remediation) does not create new tasks. The preemptive task TC-8022 has been promoted to a standard remediation task through the reconciliation process:

- It retains its original description (bump tokio to 1.42.0 in stream rhtpa-2.1)
- It retains its "Related" link to TC-8020 (cross-stream provenance)
- It gains a "Depend" link from TC-8021 (the authoritative CVE Jira for this stream)
- The `security-preemptive` label is removed, leaving labels: `ai-generated-jira`, `Security`, `CVE-2026-55123`

### Triage Decision

**Case A: Affected -- remediation task already exists (reconciled from preemptive)**

- Stream 2.1.x versions (RHTPA 2.1.0, RHTPA 2.1.1) are affected (tokio versions before 1.42.0 are shipped)
- No new remediation tasks are created
- TC-8022 serves as the remediation task, now properly linked to TC-8021
- The `ai-cve-triaged` label would be added to TC-8021 to mark triage as complete

### Final Issue State

**TC-8021** (CVE Jira):
- Status: Assigned
- Labels: CVE-2026-55123, pscomponent:org/rhtpa-server, ai-cve-triaged
- Affects Versions: RHTPA 2.1.0, RHTPA 2.1.1 (verified correct per lock file analysis)
- Issue Links: Depend --> TC-8022

**TC-8022** (Remediation Task):
- Status: Open
- Labels: ai-generated-jira, Security, CVE-2026-55123 (security-preemptive removed)
- Issue Links: Related --> TC-8020, Depend <-- TC-8021
