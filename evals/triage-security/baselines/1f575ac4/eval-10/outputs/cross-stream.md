# Cross-Stream Impact Analysis

## Cross-Stream Impact Comment (posted to TC-8020)

```
Cross-stream impact: tokio < 1.42.0 also affects stream(s) rhtpa-2.1 based on
lock file analysis. These streams are tracked by companion issues (see Related
links) or may require separate PSIRT triage.

Version impact across streams:

| Version     | Stream    | tokio version | Affected? |
|-------------|-----------|---------------|-----------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0        | YES       |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0        | YES       |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1        | YES       |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1        | YES       |

Fix threshold: tokio >= 1.42.0
```

## Sibling CVE Jira Search Results

A JQL search was performed for sibling Vulnerability issues:

```
project = TC AND labels = 'CVE-2026-55123' AND issuetype = 10024 AND key != TC-8020
```

**Result**: No sibling Vulnerability issues found for CVE-2026-55123 in stream rhtpa-2.1.

This means stream rhtpa-2.1 has no dedicated CVE Jira tracking this vulnerability.

## Step 7 Case B: Preemptive Task Creation

Since stream rhtpa-2.1 is affected but has no CVE Jira, Step 7 Case B applies.
Proactive preemptive remediation tasks are created for this stream.

### Preemptive Task Details

#### Preemptive Upstream Backport Task (rhtpa-2.1)

- **Summary**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)
- **Labels**: `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`
- **Link to TC-8020**: "Related" (not "Depend") -- because TC-8020 belongs to a different stream (rhtpa-2.2)
- **Description prefix**:
  > **Preemptive remediation**: This task was created proactively from cross-stream
  > impact analysis of TC-8020 (stream rhtpa-2.2).
  > No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
  > this task will be linked and the `security-preemptive` label removed.
- **Repository**: rhtpa-backend
- **Target Branch**: release/0.3.z
- **Affected versions**: RHTPA 2.1.0, RHTPA 2.1.1

#### Preemptive Downstream Propagation Task (rhtpa-2.1)

- **Summary**: Propagate CVE-2026-55123 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
- **Labels**: `["ai-generated-jira", "Security", "CVE-2026-55123", "security-preemptive"]`
- **Link to TC-8020**: "Related" (not "Depend") -- because TC-8020 belongs to a different stream (rhtpa-2.2)
- **Description prefix**:
  > **Preemptive remediation**: This task was created proactively from cross-stream
  > impact analysis of TC-8020 (stream rhtpa-2.2).
  > No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
  > this task will be linked and the `security-preemptive` label removed.
- **Repository**: rhtpa-release.0.3.z
- **Target Branch**: main
- **Blocked by**: preemptive upstream backport task (Blocks link)

### Preemptive Comment (posted to TC-8020)

```
Preemptive remediation tasks created for streams without CVE Jiras:
- rhtpa-2.1: <preemptive-upstream-task-key> (security-preemptive, upstream backport)
- rhtpa-2.1: <preemptive-downstream-task-key> (security-preemptive, downstream propagation)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

## Key Differences: Standard (Case A) vs Preemptive (Case B)

| Aspect | Case A (rhtpa-2.2) | Case B (rhtpa-2.1) |
|--------|-------------------|-------------------|
| Stream | rhtpa-2.2 (in scope) | rhtpa-2.1 (cross-stream) |
| Labels | ai-generated-jira, Security, CVE-2026-55123 | ai-generated-jira, Security, CVE-2026-55123, **security-preemptive** |
| Link type to TC-8020 | **Depend** | **Related** |
| Description prefix | (none) | Preemptive remediation note citing TC-8020 |
| CVE Jira exists? | Yes (TC-8020) | No |
| Reconciliation | N/A | Step 4.4 will reconcile when PSIRT creates CVE Jira for rhtpa-2.1 |

## Reconciliation Path (Future Step 4.4)

When PSIRT eventually creates a CVE Jira for CVE-2026-55123 scoped to stream rhtpa-2.1, the triage-security skill's Step 4.4 (Preemptive task reconciliation) will:

1. Search for tasks with label `security-preemptive` and `CVE-2026-55123`
2. Find the preemptive tasks created here
3. Link the new CVE Jira to the preemptive tasks with "Depend" link
4. Remove the `security-preemptive` label from the tasks
5. Skip creating new remediation tasks (preemptive tasks are now standard remediation tasks)
