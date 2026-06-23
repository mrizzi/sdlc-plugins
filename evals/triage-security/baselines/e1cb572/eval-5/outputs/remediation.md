# Step 7 -- Remediation

## Triage Outcome

**Case A applies**: Supported versions in the 2.2.x stream are affected (2.2.0, 2.2.1, 2.2.2). Remediation task creation is needed.

**Case B also applies**: Cross-stream impact detected. The 2.1.x stream (versions 2.1.0 and 2.1.1) is also affected. This will be reported via cross-stream impact comment and, if no sibling CVE Jira exists for 2.1.x, preemptive remediation tasks will be created.

## Ecosystem and Task Count

- Ecosystem: RPM (system package)
- Task count: **1 task** per affected stream (no upstream backport needed for RPM packages)
- The fix happens directly in the Konflux release repo by updating rpms.lock.yaml

## Remediation Task for 2.2.x Stream

Since versions 2.2.3 and 2.2.4 already ship the fixed openssl-libs 3.0.7-28.el9_4, the remediation is only relevant if a z-stream respin of 2.2.0, 2.2.1, or 2.2.2 is needed. However, the standard remediation path is to create a task to ensure the fix is tracked.

### Proposed Task

**Summary**: Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-40215`

**Description**:

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

A buffer over-read vulnerability exists in openssl-libs versions before 3.0.7-28.el9_4
during X.509 certificate chain verification (CVSS 7.1 High). A remote attacker can
craft a certificate with a malformed Subject Alternative Name extension that triggers
an out-of-bounds read.

Affected versions in the 2.2.x stream:
- 2.2.0 (build 0.4.5): openssl-libs 3.0.7-25.el9_3
- 2.2.1 (build 0.4.8): openssl-libs 3.0.7-27.el9_4
- 2.2.2 (build 0.4.9): openssl-libs 3.0.7-27.el9_4 (retag of 2.2.1)

Already fixed in:
- 2.2.3 (build 0.4.11): openssl-libs 3.0.7-28.el9_4
- 2.2.4 (build 0.4.12): openssl-libs 3.0.7-28.el9_4

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Package origin: explicit install (openssl-libs is present in rpms.lock.yaml)
- Update the openssl-libs package spec in rpms.in.yaml (or equivalent input file)
  to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml to pin the updated version
- The patched RPM is available via RHSA-2026:4021
- Note: versions 2.2.3+ already ship the fix -- this task ensures the fix is
  tracked for any z-stream respins of affected versions

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated openssl-libs

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
```

### Proposed Jira API Call

```
task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)",
  description: <task-description-above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215"]
)

jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: <task-key>,
  type: "Depend"
)
```

## Cross-Stream Impact (Case B)

The 2.1.x stream is also affected:
- 2.1.0 (build 0.3.8): openssl-libs 3.0.7-24.el9
- 2.1.1 (build 0.3.12): openssl-libs 3.0.7-24.el9

### Proposed Actions

1. **Search for sibling CVE Jira** for the 2.1.x stream:
   ```
   jira.search_jql(
     "project = TC AND labels = 'CVE-2026-40215' AND issuetype = 10024 AND key != TC-8005"
   )
   ```

2. **If no sibling CVE Jira exists for 2.1.x**: create a preemptive remediation task:

   **Summary**: Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.1)
   **Labels**: `ai-generated-jira`, `Security`, `CVE-2026-40215`, `security-preemptive`

   ```
   ## Repository

   rhtpa-release.0.3.z

   ## Target Branch

   main

   ## Description

   > **Preemptive remediation**: This task was created proactively from cross-stream
   > impact analysis of TC-8005 (stream rhtpa-2.2). No stream-specific CVE Jira
   > exists yet for this stream. When PSIRT creates one, this task will be linked
   > and the `security-preemptive` label removed.

   Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

   Affected versions in the 2.1.x stream:
   - 2.1.0 (build 0.3.8): openssl-libs 3.0.7-24.el9
   - 2.1.1 (build 0.3.12): openssl-libs 3.0.7-24.el9

   Advisory: https://access.redhat.com/errata/RHSA-2026:4021

   ## Implementation Notes

   - Package origin: explicit install (openssl-libs is present in rpms.lock.yaml)
   - Update the openssl-libs package spec in rpms.in.yaml (or equivalent input file)
     to >= 3.0.7-28.el9_4
   - Regenerate rpms.lock.yaml to pin the updated version

   ## Acceptance Criteria

   - [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
   - [ ] Konflux rebuild triggers new container image

   ## Test Requirements

   - [ ] Container image builds successfully with the updated openssl-libs

   ## Dependencies

   - Depends on: TC-8005 (parent tracking issue)
   ```

   Link with "Related" (not "Depend") to TC-8005.

3. **If a sibling CVE Jira exists for 2.1.x**: skip preemptive task creation for that stream.

4. **Post cross-stream impact comment on TC-8005**:
   ```
   Cross-stream impact: openssl-libs (versions before 3.0.7-28.el9_4) also affects
   stream 2.1.x based on rpms.lock.yaml analysis. This stream is tracked by companion
   issues (see Related links) or may require separate PSIRT triage.
   ```

## Post-Triage Summary

After all actions are confirmed and executed:

1. **Add label** `ai-cve-triaged` to TC-8005
2. **Post summary comment** on TC-8005 documenting:
   - Version impact table (2.2.x scoped, plus cross-stream 2.1.x)
   - Affects Versions correction: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
   - Remediation task created for 2.2.x stream
   - Cross-stream impact noted for 2.1.x stream
   - Any preemptive tasks created for 2.1.x
3. **Transition** TC-8005 to In Progress
4. **Assign** TC-8005 to current user
