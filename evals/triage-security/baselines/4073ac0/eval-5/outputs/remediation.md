# Step 7 -- Remediation

## Triage Outcome

**Case A: Affected -- create remediation task.**

Versions 2.2.0, 2.2.1, and 2.2.2 in the 2.2.x stream ship a vulnerable version of openssl-libs (< 3.0.7-28.el9_4). Versions 2.2.3 and 2.2.4 already ship the fixed version.

**Ecosystem**: RPM (system package) -- single task in the Konflux release repo. No upstream backport task needed.

**Dependency chain**: openssl-libs is an explicit install (present in rpms.lock.yaml).

## Remediation Task Description

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

A buffer over-read in X.509 certificate verification affects openssl-libs versions before 3.0.7-28.el9_4 (CVSS 7.1 High). Product versions 2.2.0 through 2.2.2 ship vulnerable versions of openssl-libs. Versions 2.2.3 and 2.2.4 already include the fixed package.

Affected versions: RHTPA 2.2.0 (openssl-libs 3.0.7-25.el9_3), RHTPA 2.2.1 (openssl-libs 3.0.7-27.el9_4), RHTPA 2.2.2 (retag of 2.2.1).

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Update the openssl-libs package version in rpms.lock.yaml (or rpms.in.yaml) to >= 3.0.7-28.el9_4
- If lock file exists: regenerate rpms.lock.yaml
- openssl-libs is an explicit install (present in rpms.lock.yaml), so update the package spec directly
- Verify the Konflux build pipeline triggers successfully after the update

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated package

## Dependencies

- Depends on: TC-8005 (parent tracking issue)

---

## Jira Linkage

```
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: "<new-task-key>",
  type: "Depend"
)
```

## Cross-Stream Impact Notice (Case B)

The 2.1.x stream is also affected (openssl-libs 3.0.7-24.el9 in both 2.1.0 and 2.1.1). A comment would be posted to TC-8005:

> Cross-stream impact: openssl-libs < 3.0.7-28.el9_4 also affects stream 2.1.x based on lock file analysis. This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.
