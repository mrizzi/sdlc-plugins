# Triage Outcome: TC-8021

## Summary

**Issue**: TC-8021 -- CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.1]
**CVE**: CVE-2026-55123
**Library**: tokio (Cargo/Rust ecosystem)
**Fix threshold**: 1.42.0
**Stream scope**: 2.1.x (rhtpa-2.1)
**CVSS**: 8.1 (High)

## Outcome: Preemptive Task Reconciled -- No New Tasks Created

The triage of TC-8021 concluded with **preemptive task reconciliation** rather than new remediation task creation. An existing preemptive remediation task (TC-8022) already covered CVE-2026-55123 for stream 2.1.x.

## How the Preemptive Task Was Reconciled

### Background

1. **TC-8020** was the first CVE Jira created by PSIRT for CVE-2026-55123, scoped to stream **rhtpa-2.2** (suffix `[rhtpa-2.2]`).

2. During triage of TC-8020, Step 2 (Version Impact Analysis) identified that stream **2.1.x** was also affected by the vulnerability (tokio < 1.42.0 was present in builds v0.3.8 and v0.3.12).

3. Step 8 Case B (Cross-stream impact) detected that stream 2.1.x had no CVE Jira of its own. Per the Case B procedure, it created **TC-8022** as a **preemptive remediation task** for stream 2.1.x with:
   - Labels: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
   - Link: "Related" to TC-8020 (the originating CVE from the other stream)

4. Later, PSIRT created **TC-8021** as the stream-specific CVE Jira for CVE-2026-55123 scoped to stream **rhtpa-2.1**.

### Reconciliation During TC-8021 Triage

When TC-8021 was triaged, Step 4.4 (Preemptive Task Reconciliation) performed a JQL search:

```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-55123'
```

This returned TC-8022, whose summary contains `(rhtpa-2.1)` matching the current issue's stream. The reconciliation procedure then:

1. **Linked** TC-8021 to TC-8022 with "Depend" -- establishing the standard CVE-to-remediation linkage
2. **Removed** the `security-preemptive` label from TC-8022 -- promoting it from preemptive to standard remediation
3. **Recorded** that remediation exists for stream 2.1.x -- preventing Step 8 from creating duplicate tasks

### Result

TC-8022 was seamlessly promoted from a preemptive remediation task to a standard remediation task. No new tasks were created because the existing preemptive task already contained the correct remediation instructions (bump tokio to 1.42.0 on the release/0.3.z branch in the backend repository).

## Final Issue Link Graph

```
TC-8020 (CVE Jira, stream rhtpa-2.2)
  |
  | Related
  v
TC-8022 (Remediation Task: bump tokio to 1.42.0, stream rhtpa-2.1)
  ^
  | Depend
  |
TC-8021 (CVE Jira, stream rhtpa-2.1)
```

- TC-8021 **Depend** -> TC-8022: standard remediation linkage (the CVE depends on the remediation task for resolution)
- TC-8022 **Related** <-> TC-8020: cross-stream provenance (TC-8022 was originally created from TC-8020's cross-stream analysis)

## Label State After Reconciliation

**TC-8022 labels (before)**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
**TC-8022 labels (after)**: `ai-generated-jira`, `Security`, `CVE-2026-55123`

The `security-preemptive` label was removed because TC-8022 is now backed by its own stream-specific CVE Jira (TC-8021).

## Step 8 Impact

Because Step 4.4 recorded that remediation already exists for stream 2.1.x (via TC-8022), Step 8 (Remediation) **skipped task creation** for this stream entirely. This is the correct behavior -- creating a new remediation task would have been a duplicate of TC-8022.

## Remaining Triage Actions

The following standard triage actions still apply to TC-8021 regardless of the preemptive reconciliation:

- **Step 3**: Affects Versions correction (verify RHTPA 2.1.0 and RHTPA 2.1.1 are correct)
- **Step 5**: Version lifecycle check (verify 2.1.x is still supported)
- **Step 0.7**: Assign and transition to Assigned
- **Post-triage**: Add `ai-cve-triaged` label, post summary comment with version impact table and reconciliation details
