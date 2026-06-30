# Step 7 -- Remediation Task

## Triage Outcome: Case A -- Affected, create remediation task

The 2.2.x stream has affected versions (2.2.0, 2.2.1, 2.2.2). A single remediation task is created because openssl-libs is an RPM system package ecosystem (not a source dependency). RPM packages do not require an upstream backport task -- the fix happens directly in the Konflux release repo.

## Task: Single System Package Remediation Task

### Jira Creation Call

```
task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215"]
)
```

### Task Description

```
## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

A buffer over-read vulnerability was found in openssl-libs versions before
3.0.7-28.el9_4 during X.509 certificate chain verification. A remote attacker
can craft a certificate with a malformed extension that triggers an
out-of-bounds read (CVSS 7.1 High).

Affected versions in the 2.2.x stream:
- 2.2.0 (v0.4.5): openssl-libs 3.0.7-25.el9_3
- 2.2.1 (v0.4.8): openssl-libs 3.0.7-27.el9_4
- 2.2.2 (v0.4.9): retag of 2.2.1

Already fixed in:
- 2.2.3 (v0.4.11): openssl-libs 3.0.7-28.el9_4
- 2.2.4 (v0.4.12): openssl-libs 3.0.7-28.el9_4

Package origin: explicit install (present in rpms.lock.yaml)

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Update the openssl-libs package version in rpms.in.yaml to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml to pick up the updated version
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)
```

**Note**: Files to Modify section is intentionally omitted per remediation-templates.md. These depend on repository structure that the triage skill does not have context for -- `/implement-task` discovers them via code analysis.

### Post-Creation Actions

1. **Description digest comment**: Post digest comment to the new task before any links or other comments.
2. **Link** the task to TC-8005:
   ```
   jira.create_link(
     inwardIssue: "TC-8005",
     outwardIssue: <task-key>,
     type: "Depend"
   )
   ```
3. **Transition** TC-8005 to In Progress.
4. **Assign** TC-8005 to the current user.
5. **Post comment** to TC-8005: "Remediation task created: [task-key]"

### Why a Single Task (Not Two)

RPM is a system package ecosystem. The remediation happens directly in the Konflux release repo (`rhtpa-release.0.4.z`) by updating the package specification and regenerating the lock file. There is no upstream source repository to patch first -- unlike Cargo/npm/Go source dependencies which require a two-task flow (upstream backport + downstream propagation), RPM system packages need only one task targeting the Konflux release repo.
