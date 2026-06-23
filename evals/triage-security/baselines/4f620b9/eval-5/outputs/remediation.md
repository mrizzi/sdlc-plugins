# Step 7 - Remediation

## Triage Outcome: Case A - Affected (create remediation task)

Versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream ship vulnerable openssl-libs. Since the ecosystem is RPM and the package is an explicit install (present in rpms.lock.yaml), a **single** remediation task is created for the Konflux release repo. No upstream backport task is needed.

## Proposed Remediation Task

**Summary**: Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)

**Labels**: ai-generated-jira, Security, CVE-2026-40215

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

A buffer over-read vulnerability in X.509 certificate verification affects openssl-libs versions before 3.0.7-28.el9_4 (CVSS 7.1 High). Versions 2.2.0, 2.2.1, and 2.2.2 ship vulnerable openssl-libs and must be updated.

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Update the openssl-libs package version in rpms.in.yaml (or equivalent package spec) to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml to reflect the updated package version
- Verify the Konflux build pipeline triggers successfully with the updated RPM

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)

---

## Proposed Jira API Calls

The following Jira mutations would be executed after engineer confirmation:

### 1. Create remediation task

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)",
  description: <task-description-above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215"]
)
```

### 2. Link task to Vulnerability issue

```
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: "<new-task-key>",
  type: "Depend"
)
```

### 3. Transition Vulnerability to In Progress

```
jira.transition_issue("TC-8005", "In Progress")
```

### 4. Add ai-cve-triaged label

```
jira.edit_issue("TC-8005", {
  "labels": ["CVE-2026-40215", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### 5. Post triage summary comment to TC-8005

```
Remediation task created: <new-task-key> (Konflux release repo update for openssl-libs in 2.2.x stream)

Cross-stream impact: openssl-libs versions before 3.0.7-28.el9_4 also affects stream 2.1.x
based on rpms.lock.yaml analysis (3.0.7-24.el9 at both 2.1.0 and 2.1.1). That stream is
tracked by its own PSIRT-created Vulnerability issue or may require separate PSIRT triage.
```

**Note**: All proposed actions above are presented for engineer confirmation. No Jira mutations would be executed without explicit approval.
