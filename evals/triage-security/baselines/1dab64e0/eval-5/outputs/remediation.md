# Step 8 -- Remediation

## Triage Outcome: Case A + Case B

**Case A** -- The 2.2.x stream (issue scope) has affected versions (2.2.0,
2.2.1, 2.2.2). Create a remediation task for the 2.2.x stream.

**Case B** -- Cross-stream impact: the 2.1.x stream is also fully affected
(all versions ship openssl-libs 3.0.7-24.el9). A cross-stream impact comment
would be posted, and if no companion CVE Jira exists for the 2.1.x stream,
a preemptive remediation task would be created with the `security-preemptive`
label.

## Remediation Task -- 2.2.x Stream (Case A, System Package / Explicit Install)

### Jira Creation Call

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)",
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

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

A buffer over-read vulnerability in openssl-libs during X.509 certificate
chain verification affects versions before 3.0.7-28.el9_4. The package
is explicitly installed via rpms.lock.yaml in the Konflux release repo.

Affected versions: RHTPA 2.2.0 (3.0.7-25.el9_3), RHTPA 2.2.1 (3.0.7-27.el9_4),
RHTPA 2.2.2 (retag of 2.2.1, 3.0.7-27.el9_4)

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Update openssl-libs to >= 3.0.7-28.el9_4 in rpms.in.yaml or the package spec
- Regenerate rpms.lock.yaml to pin the updated version
- The package is an explicit install (confirmed present in rpms.lock.yaml)
- SBOM verification was skipped (cosign not available); classification based on rpms.lock.yaml only
- Verify the Konflux build pipeline triggers successfully after the update

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4 in rpms.lock.yaml
- [ ] Konflux rebuild triggers new container image
- [ ] No other package conflicts introduced

## Test Requirements

- [ ] Container image builds successfully with the updated package

## Dependencies

- Depends on: TC-8005 (parent Vulnerability tracking issue)

---

## Cross-Stream Impact Comment (Case B)

The following comment would be posted to TC-8005:

```
Cross-stream impact: openssl-libs (versions before 3.0.7-28.el9_4)
also affects stream 2.1.x based on rpms.lock.yaml analysis.

2.1.x versions affected:
- 2.1.0 (v0.3.8): openssl-libs 3.0.7-24.el9
- 2.1.1 (v0.3.12): openssl-libs 3.0.7-24.el9

This stream is tracked by a companion issue (see Related links)
or may require separate PSIRT triage.
```

## Preemptive Remediation Task -- 2.1.x Stream (Case B)

If no companion CVE Jira exists for the 2.1.x stream, a preemptive
remediation task would be created:

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.1)",
  description: <preemptive variant of system package template>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215", "security-preemptive"]
)
```

The preemptive task would use:
- Link type: "Related" (not "Depend") to TC-8005
- Description prefix noting originating CVE TC-8005 from stream 2.2.x
- Repository: rhtpa-release.0.3.z
- Target: update openssl-libs to >= 3.0.7-28.el9_4 in rpms.lock.yaml

## Jira Linkage (would execute after task creation)

```
# Link 2.2.x remediation task to vulnerability issue
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: "<2.2.x-task-key>",
  type: "Depend"
)

# Link preemptive 2.1.x task (if created) as Related
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: "<2.1.x-preemptive-task-key>",
  type: "Related"
)
```
