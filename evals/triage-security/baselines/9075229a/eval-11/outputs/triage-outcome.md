# Triage Outcome: TC-8021

## Summary

TC-8021 (CVE-2026-55123 tokio use-after-free, stream rhtpa-2.1) was triaged with
preemptive task reconciliation as the primary outcome. An existing preemptive remediation
task (TC-8022) was found and reconciled, eliminating the need to create new remediation
tasks.

## Issue Details

| Field | Value |
|-------|-------|
| Issue | TC-8021 |
| CVE | CVE-2026-55123 |
| Library | tokio |
| Fixed version | 1.42.0 |
| Stream scope | 2.1.x (from suffix `[rhtpa-2.1]`) |
| Ecosystem | Cargo |
| Severity | 8.1 / High |

## Reconciliation Outcome

Step 4.4 (Preemptive Task Reconciliation) found TC-8022, a preemptive remediation task
that exactly matches this CVE and stream. The task was created during prior triage of
TC-8020 (the companion CVE Jira for stream rhtpa-2.2), which identified cross-stream
impact on the 2.1.x stream via Step 8 Case B.

### What happened

1. **Search**: JQL query for tasks with labels `security-preemptive` and `CVE-2026-55123`
   returned TC-8022.
2. **Stream filter**: TC-8022's summary contains `(rhtpa-2.1)`, matching TC-8021's stream
   scope. The task is confirmed as the correct preemptive task for this stream.
3. **Link creation**: A "Depend" link was created from TC-8021 to TC-8022, establishing
   the standard remediation dependency (same link type used when triage-security creates
   new remediation tasks in Step 8).
4. **Label removal**: The `security-preemptive` label was removed from TC-8022. The task
   is now a standard remediation task linked to its proper CVE Jira.
5. **Reconciliation recorded**: Step 8 skips remediation task creation for the 2.1.x
   stream because TC-8022 already covers it.

### Why no new remediation tasks were created

The preemptive task TC-8022 already contains the correct remediation scope:
- Bumps tokio to 1.42.0 (the fix threshold)
- Targets the rhtpa-2.1 stream
- Was created with the same task description template used by standard remediation

Creating a new task would produce a duplicate. The reconciliation process converts the
preemptive task into a standard remediation task by:
- Adding the "Depend" link from TC-8021 (making TC-8022 the remediation for this CVE Jira)
- Removing the `security-preemptive` label (the task is no longer preemptive)

### Link topology after reconciliation

```
TC-8020 (CVE-2026-55123, stream rhtpa-2.2)
  |
  +--[Related]--> TC-8022 (remediation task, originally preemptive)
                    |
TC-8021 (CVE-2026-55123, stream rhtpa-2.1)
  |
  +--[Depend]---> TC-8022 (now standard remediation task)
```

TC-8022 retains its "Related" link to TC-8020 (the originating CVE Jira that created it)
and gains a "Depend" link from TC-8021 (the stream-specific CVE Jira it now serves).

## Step 8 Disposition

**No new remediation tasks created.** The preemptive task TC-8022 was reconciled as the
standard remediation task for TC-8021. Step 8 Case A task creation is skipped for the
2.1.x stream because reconciliation in Step 4.4 recorded that remediation already exists.

## Post-Triage Actions

The following post-triage actions would be performed (pending engineer confirmation):

1. **Add `ai-cve-triaged` label** to TC-8021 to mark it as triaged
2. **Post summary comment** on TC-8021 documenting:
   - Version impact analysis for 2.1.x stream
   - Affects Versions verification (RHTPA 2.1.0, RHTPA 2.1.1)
   - Preemptive task reconciliation outcome (TC-8022 linked and promoted)
   - @mention of the issue reporter (PSIRT analyst)
