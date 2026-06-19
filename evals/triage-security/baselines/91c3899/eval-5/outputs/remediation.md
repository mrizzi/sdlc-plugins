# Step 7 -- Remediation

## Triage Outcome: Case A -- Affected versions exist, create remediation task

Versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream ship a vulnerable version of openssl-libs (below 3.0.7-28.el9_4). The fix is already present in versions 2.2.3 and 2.2.4, so the remediation is a lock file update for builds targeting affected versions.

## Ecosystem: RPM -- Single Task

Because openssl-libs is an RPM system package (not a source dependency like Cargo/npm/Go), the remediation follows the **single task** pattern. The fix happens directly in the Konflux release repo. There is no upstream backport + downstream propagation split.

## Package Origin: Explicit Install

openssl-libs is present in `rpms.lock.yaml` (confirmed in Step 2.3.5), so it is an explicitly installed package. The remediation template for explicit install origin applies.

## Remediation Task Description

The following task description would be created as a Jira Task:

**Summary**: Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)

**Labels**: ai-generated-jira, Security, CVE-2026-40215

---

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

## Implementation Notes

- Update the package version in Dockerfile (dnf install command or package spec)
- If lock file exists: regenerate rpms.lock.yaml

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image

## Dependencies

- Depends on: TC-8005 (parent tracking issue)

---

## Jira API Call (pending engineer confirmation)

```
task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)",
  description: <task-description-above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215"]
)
```

## Jira Linkage

```
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: <task-key>,
  type: "Depend"
)
```

Note: Only one task is created because this is an RPM ecosystem vulnerability. Source dependency ecosystems (Cargo, npm, Go) would produce two tasks (upstream backport + downstream propagation), but RPM packages are fixed directly in the Konflux release repo.
