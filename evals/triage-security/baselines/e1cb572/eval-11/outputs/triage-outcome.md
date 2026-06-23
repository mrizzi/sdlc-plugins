# Triage Outcome -- TC-8021

## Summary

**Issue**: TC-8021 -- CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1]
**CVE**: CVE-2026-55123 (CVSS 8.1 High)
**Library**: tokio (Cargo/Rust ecosystem)
**Affected range**: versions before 1.42.0
**Fixed version**: 1.42.0
**Stream scope**: rhtpa-2.1 (2.1.x)

## Triage Decision: Reconcile with Existing Preemptive Task

This triage concluded with **preemptive task reconciliation** rather than new remediation task creation. The full reasoning follows.

## How the Preemptive Task Was Reconciled

### Background

1. **TC-8020** was the first CVE Jira created by PSIRT for CVE-2026-55123, scoped to stream rhtpa-2.2 (2.2.x).
2. During the triage of TC-8020, the version impact analysis (Step 2) identified that stream 2.1.x was also affected by the same vulnerability.
3. Per Step 7 Case B (cross-stream impact / proactive remediation), since no CVE Jira existed for stream 2.1.x at that time, a **preemptive remediation task TC-8022** was created with:
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
   - Link: Related to TC-8020 (originating CVE)
   - Summary: "Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)"

4. Subsequently, PSIRT created **TC-8021** as the stream-specific CVE Jira for rhtpa-2.1.

### Reconciliation Process (Step 4.4)

When triaging TC-8021, Step 4.4 searched for preemptive tasks matching CVE-2026-55123:

```
JQL: project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123'
Result: TC-8022 (summary contains "rhtpa-2.1" -- matches current stream)
```

Since TC-8022 is a preemptive task for the same CVE and the same stream as TC-8021, reconciliation applies:

### Proposed Jira Mutations (pending engineer confirmation)

1. **Link TC-8021 to TC-8022 with "Depend"**
   - Establishes the standard remediation linkage between the CVE Jira and its remediation task
   - TC-8022 is now the official remediation task for TC-8021

2. **Remove `security-preemptive` label from TC-8022**
   - Current labels: `[ai-generated-jira, Security, CVE-2026-55123, security-preemptive]`
   - Updated labels: `[ai-generated-jira, Security, CVE-2026-55123]`
   - The task transitions from preemptive to standard remediation status

3. **Preserve existing "Related" link from TC-8022 to TC-8020**
   - The cross-stream traceability link remains intact
   - Provides audit trail showing the task's origin

4. **Skip new remediation task creation in Step 7**
   - TC-8022 already covers the required remediation (bump tokio to 1.42.0)
   - No duplicate task is needed

5. **Add `ai-cve-triaged` label to TC-8021**
   - Marks the Vulnerability issue as triaged

6. **Post triage summary comment to TC-8021** documenting:
   - Version impact table (RHTPA 2.1.0 and 2.1.1 both affected)
   - Affects Versions confirmation (RHTPA 2.1.0, RHTPA 2.1.1 -- matches PSIRT assignment)
   - Reconciliation with preemptive task TC-8022
   - Link to companion CVE TC-8020 (stream rhtpa-2.2)

## Final Link Topology

```
TC-8020 (CVE Jira, rhtpa-2.2)
  |
  +--[Related]--> TC-8022 (remediation task, rhtpa-2.1)
                    |
TC-8021 (CVE Jira, rhtpa-2.1)
  |
  +--[Depend]---> TC-8022 (remediation task, rhtpa-2.1)
  |
  +--[Related]--> TC-8020 (companion CVE, rhtpa-2.2, via Step 4.2)
```

TC-8022 serves as the single remediation task for rhtpa-2.1, linked to both the originating cross-stream CVE (TC-8020 via Related) and the now-existing stream-specific CVE (TC-8021 via Depend).

## Affects Versions Assessment

The PSIRT-assigned Affects Versions (RHTPA 2.1.0, RHTPA 2.1.1) align with the version impact analysis for stream 2.1.x. Both versions ship tokio at a version below the 1.42.0 fix threshold. No correction is needed.

## Steps Not Requiring Action

- **Step 4.1 (Same-stream duplicates)**: No same-stream siblings found -- TC-8020 is a different-stream companion (rhtpa-2.2), not a duplicate.
- **Step 4.2 (Cross-stream coordination)**: TC-8020 is a different-stream companion. Propose creating a "Related" link between TC-8021 and TC-8020 if not already linked.
- **Step 4.3 (Cross-CVE overlap)**: No other CVEs affecting tokio in the same PS Component and stream were identified.
- **Step 5 (Lifecycle check)**: Assumed both 2.1.x versions are within support lifecycle (would be verified via Product pages URL in a live triage).
- **Step 6 (Already fixed check)**: TC-8020 (rhtpa-2.2) is not resolved, so no already-fixed scenario applies.
- **Step 7 (Remediation task creation)**: Skipped -- reconciliation in Step 4.4 identified TC-8022 as the existing remediation task. No new tasks needed.
