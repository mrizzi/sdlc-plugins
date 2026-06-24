# Step 7 -- Remediation

## Triage Outcome: Case A + Case B

The 2.2.x stream has affected versions (2.2.0, 2.2.1, 2.2.2), so remediation tasks are needed. Additionally, the 2.1.x stream is also affected (cross-stream impact, Case B).

Since openssl-libs is an RPM (system package ecosystem), a **single remediation task** is created per affected stream (no upstream backport step).

## Remediation Task -- 2.2.x Stream (Case A: scoped stream)

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215"]
)
```

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to include the fix for a buffer over-read in X.509 certificate verification.

The vulnerable package (openssl-libs, versions before 3.0.7-28.el9_4) is present in the 2.2.x stream's rpms.lock.yaml. Versions 2.2.0, 2.2.1, and 2.2.2 ship vulnerable openssl-libs. Versions 2.2.3 and 2.2.4 already ship the fixed version 3.0.7-28.el9_4.

Affected versions:
- RHTPA 2.2.0 (v0.4.5): openssl-libs 3.0.7-25.el9_3
- RHTPA 2.2.1 (v0.4.8): openssl-libs 3.0.7-27.el9_4
- RHTPA 2.2.2 (v0.4.9): retag of v0.4.8, same as 2.2.1

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-40215

Note: The fix is already present in builds 0.4.11+ (versions 2.2.3, 2.2.4). This task covers ensuring the fix is documented and that any z-stream respins of older builds would pick up the patched package. If no respin of 2.2.0-2.2.2 is planned, this task can be closed as the vulnerability is already resolved in the latest shipped versions (2.2.3+).

## Implementation Notes

- The openssl-libs package is present in rpms.lock.yaml as an explicit install
- Update the openssl-libs version spec in rpms.in.yaml (or equivalent input file) to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml to reflect the updated version
- If the base image already includes the patched openssl-libs, verify that the lock file pins are consistent

## Acceptance Criteria

- [ ] openssl-libs version in rpms.lock.yaml is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated openssl-libs version

## Dependencies

- Depends on: TC-8005 (parent Vulnerability tracking issue)

---

## Preemptive Remediation Task -- 2.1.x Stream (Case B: cross-stream impact)

The 2.1.x stream also ships vulnerable openssl-libs (3.0.7-24.el9 in both 2.1.0 and 2.1.1) but is outside the scope of TC-8005 (which is scoped to 2.2.x). A preemptive remediation task would be created for the 2.1.x stream if no sibling CVE Jira exists for that stream.

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.1.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215", "security-preemptive"]
)
```

### Preemptive Task Description

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8005 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-40215: update openssl-libs to include the fix for a buffer over-read in X.509 certificate verification.

The vulnerable package (openssl-libs, versions before 3.0.7-28.el9_4) is present in the 2.1.x stream's rpms.lock.yaml. Both shipped versions are affected:
- RHTPA 2.1.0 (v0.3.8): openssl-libs 3.0.7-24.el9
- RHTPA 2.1.1 (v0.3.12): openssl-libs 3.0.7-24.el9

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- The openssl-libs package is present in rpms.lock.yaml as an explicit install
- Update the openssl-libs version spec in rpms.in.yaml (or equivalent input file) to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml to reflect the updated version
- If the base image already includes the patched openssl-libs, verify that the lock file pins are consistent

## Acceptance Criteria

- [ ] openssl-libs version in rpms.lock.yaml is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated openssl-libs version

## Dependencies

- Depends on: TC-8005 (related Vulnerability tracking issue -- cross-stream)

---

## Linkage

### 2.2.x remediation task (Case A):
```
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: "<2.2.x-task-key>",
  type: "Depend"
)
```

### 2.1.x preemptive remediation task (Case B):
```
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: "<2.1.x-preemptive-task-key>",
  type: "Related"
)
```

## Cross-Stream Impact Comment (would post to TC-8005)

```
Cross-stream impact: openssl-libs (versions before 3.0.7-28.el9_4) also affects stream 2.1.x based on rpms.lock.yaml analysis.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <preemptive-task-key> (security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive label.
When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link
them and remove the label.
```
