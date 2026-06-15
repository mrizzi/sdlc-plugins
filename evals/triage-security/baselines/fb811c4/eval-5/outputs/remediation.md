# Remediation Task — TC-8005 (CVE-2026-40215)

## Ecosystem and Task Flow

- **Ecosystem**: RPM (system package)
- **Task flow**: Single task (RPM ecosystems do not use the two-task upstream backport + downstream propagation flow)
- **Package origin**: Explicit install (openssl-libs is present in rpms.lock.yaml)
- **Template**: System package task -- explicit install origin

## Task: Remediate CVE-2026-40215 in rhtpa-release.0.4.z

### Jira Issue Creation

```
task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)",
  description: <task-description below>,
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

## Implementation Notes

- Update the package version in Dockerfile (dnf install command or package spec)
- If lock file exists: regenerate rpms.lock.yaml
- The openssl-libs package is an explicit install (present in rpms.lock.yaml), so the version pin must be updated directly in the package spec or rpms.in.yaml and the lock file regenerated
- Advisory reference: https://access.redhat.com/errata/RHSA-2026:4021

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)

---

### Jira Linkage

```
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: <task-key>,
  type: "Depend"
)
```

After task creation:
- Transition TC-8005 to In Progress (if not already)
- Assign TC-8005 to the current user (if not already assigned)
- Add comment to TC-8005: "Remediation task created: <task-key>"
