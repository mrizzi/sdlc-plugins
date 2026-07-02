# Triage Outcome: TC-8021 -- Preemptive Task Reconciliation

## Summary

TC-8021 (CVE-2026-55123, tokio use-after-free, stream `[rhtpa-2.1]`) was triaged and reconciled with an existing preemptive remediation task. No new remediation tasks were created.

## Background

1. **TC-8020** was the first CVE Jira for CVE-2026-55123, scoped to stream `[rhtpa-2.2]`.
2. During triage of TC-8020, the cross-stream version impact analysis (Step 8 Case B) identified that stream rhtpa-2.1 was also affected by the vulnerable tokio version.
3. Since no CVE Jira existed yet for rhtpa-2.1, the triage of TC-8020 created a **preemptive remediation task** (TC-8022) for the rhtpa-2.1 stream, with:
   - The `security-preemptive` label to mark it as proactively created
   - A "Related" link (not "Depend") to TC-8020, the originating CVE Jira
4. Later, PSIRT created TC-8021 -- a dedicated CVE Jira for CVE-2026-55123 scoped to stream `[rhtpa-2.1]`.

## Reconciliation (Step 4.4)

When TC-8021 was triaged, Step 4.4 searched for preemptive tasks matching CVE-2026-55123 and stream rhtpa-2.1. The search found TC-8022, confirming that remediation work already existed for this stream.

### Actions Taken

1. **Linked TC-8021 to TC-8022 with "Depend"** -- This establishes the standard remediation linkage, connecting the new CVE Jira to the existing remediation task just as if the task had been created during this triage.

2. **Removed `security-preemptive` label from TC-8022** -- The task is no longer preemptive; it now has a proper CVE Jira owner. Updated labels: `ai-generated-jira`, `Security`, `CVE-2026-55123`.

3. **Recorded reconciliation** -- Step 8 task creation was skipped for the rhtpa-2.1 stream because TC-8022 already covers the required remediation (bump tokio to 1.42.0).

## Triage Decision

| Aspect | Detail |
|--------|--------|
| CVE | CVE-2026-55123 |
| Library | tokio |
| Fix threshold | 1.42.0 |
| Stream | rhtpa-2.1 (2.1.x) |
| Outcome | **Reconciled with existing preemptive task** |
| Preemptive task | TC-8022 |
| Originating triage | TC-8020 (stream rhtpa-2.2) |
| New tasks created | 0 (skipped -- remediation already exists) |
| Link created | TC-8021 --[Depend]--> TC-8022 |
| Label change | Removed `security-preemptive` from TC-8022 |

## Why This Works

The preemptive task reconciliation mechanism (Step 4.4) is the counterpart to Step 8 Case B's proactive remediation. Together they ensure:

- **No remediation gaps**: When a CVE affects multiple streams, Case B creates preemptive tasks for streams that lack their own CVE Jira, ensuring remediation starts immediately.
- **No duplicate tasks**: When PSIRT later creates a stream-specific CVE Jira, Step 4.4 finds the existing preemptive task and promotes it to a standard remediation task, avoiding creation of a duplicate.
- **Full traceability**: The "Related" link to TC-8020 (the originating triage) is preserved, while the new "Depend" link to TC-8021 establishes the standard CVE-to-remediation relationship. Both the provenance and the ownership are visible in Jira.

## Post-Reconciliation State

- **TC-8021** (CVE Jira, rhtpa-2.1): Has a "Depend" link to TC-8022. Ready for `ai-cve-triaged` label and post-triage summary comment.
- **TC-8022** (remediation task): Now a standard remediation task. Labels: `ai-generated-jira`, `Security`, `CVE-2026-55123`. Links: "Depend" from TC-8021, "Related" to TC-8020.
- **TC-8020** (CVE Jira, rhtpa-2.2): Unchanged. Retains "Related" link to TC-8022 for provenance.
