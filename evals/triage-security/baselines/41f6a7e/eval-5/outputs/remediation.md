# Step 7 -- Remediation

## Triage Outcome: Case A -- Affected (create remediation task)

Versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream ship vulnerable openssl-libs. Since openssl-libs is an RPM system package, a **single remediation task** is created (no upstream backport needed).

## Cross-Stream Impact Notice (Case B)

The 2.1.x stream is also affected (versions 2.1.0 and 2.1.1 ship openssl-libs 3.0.7-24.el9). A comment would be posted to TC-8005:

```
Cross-stream impact: openssl-libs (versions before 3.0.7-28.el9_4) also affects
stream 2.1.x based on rpms.lock.yaml analysis. This stream is tracked by a
companion issue (see Related links) or may require separate PSIRT triage.
```

## Remediation Task Description

This is the task that would be created in Jira for the 2.2.x stream. Since the package is present in rpms.lock.yaml (explicit install origin), the explicit install template applies.

### Jira Issue Creation

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)",
  description: <task-description-below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215"]
)
```

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

A buffer over-read vulnerability was found in openssl-libs during X.509 certificate chain verification. Versions before 3.0.7-28.el9_4 are vulnerable. A remote attacker can craft a certificate with a malformed extension that triggers an out-of-bounds read, potentially leaking sensitive memory contents or causing a crash.

CVSS: 7.1 (High)

Affected versions in the 2.2.x stream:
- 2.2.0 (build 0.4.5, openssl-libs 3.0.7-25.el9_3)
- 2.2.1 (build 0.4.8, openssl-libs 3.0.7-27.el9_4)
- 2.2.2 (build 0.4.9, retag of 2.2.1)

Already fixed in:
- 2.2.3 (build 0.4.11, openssl-libs 3.0.7-28.el9_4)
- 2.2.4 (build 0.4.12, openssl-libs 3.0.7-28.el9_4)

Advisory: https://access.redhat.com/errata/RHSA-2026:4021

## Implementation Notes

- Update the openssl-libs package version to >= 3.0.7-28.el9_4 in rpms.in.yaml (or equivalent package spec)
- Regenerate rpms.lock.yaml to reflect the updated version
- Note: versions 2.2.3 and 2.2.4 already ship the fixed version (3.0.7-28.el9_4), so this fix targets the next z-stream build in the 2.2.x release pipeline
- The fix is already available in RHSA-2026:4021

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] rpms.lock.yaml reflects the updated package version
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated openssl-libs

## Dependencies

- Depends on: TC-8005 (parent Vulnerability tracking issue)

---

## Jira Linkage (would execute after task creation)

```
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: "<new-task-key>",
  type: "Depend"
)
```

## Post-Creation Actions

1. Transition TC-8005 to In Progress
2. Assign TC-8005 to current user
3. Add `ai-cve-triaged` label to TC-8005
4. Post summary comment to TC-8005 documenting the triage outcome and linking the remediation task
