# Remediation (Step 7)

Ecosystem: RPM (system package) -- only one remediation task is needed. No upstream backport task required since the fix is an RPM update in the Konflux release repo.

## Proposed Jira Task

### Task: RPM Update (2.2.x stream)

- **Repository**: rhtpa-release.0.4.z (Konflux release repo from Version Streams)
- **Target Branch**: main
- **Description**: Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4
- **Implementation Notes**: update the package version in rpms.lock.yaml (or rpms.in.yaml), regenerate lock file
- **Acceptance Criteria**: openssl-libs >= 3.0.7-28.el9_4, Konflux rebuild triggers new container image

## Proposed Jira Mutation

```
jira.create_issue({
  project: "TC",
  issueType: "Task",
  summary: "CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 in rhtpa-release.0.4.z",
  description: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4\n\nRepository: rhtpa-release.0.4.z\nTarget Branch: main\nImplementation Notes: update the package version in rpms.lock.yaml (or rpms.in.yaml), regenerate lock file\nAcceptance Criteria: openssl-libs >= 3.0.7-28.el9_4, Konflux rebuild triggers new container image",
  parent: "TC-8005"
})
```

This mutation is a **proposal** and requires approval before execution.
