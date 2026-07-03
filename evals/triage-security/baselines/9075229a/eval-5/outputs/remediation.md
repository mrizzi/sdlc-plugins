# Step 8 -- Remediation: TC-8005

## Triage Outcome

**Case A**: Affected -- the issue's stream-scoped versions (2.2.0, 2.2.1, 2.2.2) are affected. Create remediation task for stream 2.2.x.

**Case B**: Cross-stream impact -- stream 2.1.x is also affected (versions 2.1.0, 2.1.1 ship openssl-libs 3.0.7-24.el9 which is within the affected range). A cross-stream impact comment would be posted and preemptive remediation tasks created for 2.1.x if no sibling CVE Jira exists for that stream.

## Ecosystem and Task Count

- Ecosystem: **RPM** (system package)
- Task count: **1 task** per affected stream (no upstream step needed for system packages)
- Package origin: **explicit install** (openssl-libs is present in rpms.lock.yaml)

## Remediation Task Description (Stream 2.2.x)

This is the task description that would be created via `jira.create_issue()`:

---

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

A buffer over-read vulnerability in openssl-libs (versions before 3.0.7-28.el9_4)
affects the X.509 certificate chain verification code path. The fix adds bounds
checking before reading extension data.

Affected versions: RHTPA 2.2.0 (3.0.7-25.el9_3), RHTPA 2.2.1 (3.0.7-27.el9_4), RHTPA 2.2.2 (retag of 2.2.1)
Fixed in: RHTPA 2.2.3+ (ships 3.0.7-28.el9_4)

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- Update the package version in rpms.in.yaml / rpms.lock.yaml to >= 3.0.7-28.el9_4
- If lock file exists: regenerate rpms.lock.yaml
- openssl-libs is an explicitly installed package (confirmed present in rpms.lock.yaml)
- SBOM verification was skipped (cosign not available) -- using rpms.lock.yaml classification only

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)

---

## Jira Issue Creation Call

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

## Cross-Stream Impact Comment (Case B)

The following comment would be posted to TC-8005:

```
Cross-stream impact: openssl-libs (versions before 3.0.7-28.el9_4) also affects
stream 2.1.x based on rpms.lock.yaml analysis:
- 2.1.0: openssl-libs 3.0.7-24.el9 (affected)
- 2.1.1: openssl-libs 3.0.7-24.el9 (affected)

These streams are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

If no sibling CVE Jira exists for stream 2.1.x, a preemptive remediation task
would be created with:
- Labels: ["ai-generated-jira", "Security", "CVE-2026-40215", "security-preemptive"]
- Link type: "Related" (not "Depend") to TC-8005
- Repository: rhtpa-release.0.3.z
- Same explicit-install template as above, targeting rpms.lock.yaml update
  for openssl-libs >= 3.0.7-28.el9_4 in the 2.1.x stream
