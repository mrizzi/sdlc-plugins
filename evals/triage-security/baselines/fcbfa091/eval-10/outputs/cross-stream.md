# Cross-Stream Impact — TC-8020

## Cross-Stream Impact Comment

The following comment would be posted to TC-8020 to document the cross-stream impact:

```
Cross-stream impact: tokio < 1.42.0 also affects stream rhtpa-2.1 based on lock file analysis.

Version impact across streams:

| Version | Stream | tokio version | Affected? |
|---------|--------|---------------|-----------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES |

Stream rhtpa-2.1 has no companion CVE Jira for CVE-2026-55123.
Preemptive remediation tasks have been created (see below).
```

## Sibling CVE Jira Search Results

JQL query:
```
project = TC AND issuetype = 10024 AND labels = "CVE-2026-55123" AND summary ~ "[rhtpa-2.1]"
```

**Result**: No issues found. No sibling CVE Jira exists for stream rhtpa-2.1.

## Preemptive Task Details

Since stream rhtpa-2.1 is affected but has no CVE Jira, preemptive remediation tasks are created per Case B:

### Preemptive Upstream Backport Task (rhtpa-2.1)

- **Summary**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
- **Link to TC-8020**: Related (not Depend -- because this is a cross-stream preemptive task)
- **Target branch**: release/0.3.z
- **Description prefix**:
  > **Preemptive remediation**: This task was created proactively from cross-stream
  > impact analysis of TC-8020 (stream rhtpa-2.2).
  > No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
  > this task will be linked and the `security-preemptive` label removed.

### Preemptive Downstream Propagation Subtask (rhtpa-2.1)

- **Summary**: Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)
- **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`
- **Link to TC-8020**: Related (not Depend)
- **Blocked by**: preemptive upstream backport task (Blocks link)
- **Description prefix**:
  > **Preemptive remediation**: This task was created proactively from cross-stream
  > impact analysis of TC-8020 (stream rhtpa-2.2).
  > No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
  > this task will be linked and the `security-preemptive` label removed.

## Preemptive Task Comment on TC-8020

The following comment would be posted to TC-8020 documenting the preemptive tasks:

```
Preemptive remediation tasks created for streams without CVE Jiras:
- rhtpa-2.1: <preemptive-upstream-task-key> (security-preemptive, upstream backport)
- rhtpa-2.1: <preemptive-downstream-task-key> (security-preemptive, downstream propagation)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

## Key Differences: Standard vs Preemptive Tasks

| Aspect | Case A (rhtpa-2.2) | Case B Preemptive (rhtpa-2.1) |
|--------|---------------------|-------------------------------|
| Labels | `ai-generated-jira`, `Security`, `CVE-2026-55123` | `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive` |
| Link to TC-8020 | Depend | Related |
| Description prefix | None | Preemptive remediation note referencing TC-8020 |
| Upstream branch | release/0.4.z | release/0.3.z |
| Konflux repo | rhtpa-release.0.4.z | rhtpa-release.0.3.z |
| Reconciliation | N/A | When PSIRT creates a rhtpa-2.1 CVE Jira, Step 4.4 links and removes `security-preemptive` label |
