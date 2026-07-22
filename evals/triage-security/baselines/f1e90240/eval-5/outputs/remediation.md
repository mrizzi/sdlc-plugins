# Step 8 -- Remediation: TC-8005

## Triage Outcome

**Case A** applies: the 2.2.x stream (scoped) has affected versions (2.2.0, 2.2.1, 2.2.2).

**Case B** also applies: the 2.1.x stream is also affected (2.1.0, 2.1.1) but
is outside this issue's scope. A cross-stream impact comment would be posted, and
preemptive remediation tasks created for the 2.1.x stream if no sibling CVE Jira
exists for that stream.

Since openssl-libs is an RPM system package (not a source dependency), a single
remediation task is created per affected stream (no upstream/downstream split).

Note: versions 2.2.3 and 2.2.4 already ship the fixed openssl-libs 3.0.7-28.el9_4.
The fix has already been incorporated into the rpms.lock.yaml for the latest builds.
The remediation task documents this and ensures verification.

---

## Remediation Task: 2.2.x stream

**Summary**: Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)

**Labels**: ai-generated-jira, Security, CVE-2026-40215

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4.

A buffer over-read vulnerability exists in openssl-libs versions before
3.0.7-28.el9_4, affecting X.509 certificate chain verification. A remote
attacker can craft a certificate with a malformed Subject Alternative Name
extension to trigger an out-of-bounds read.

Affected versions: RHTPA 2.2.0 (3.0.7-25.el9_3), RHTPA 2.2.1 (3.0.7-27.el9_4),
RHTPA 2.2.2 (retag of 2.2.1).

Note: versions 2.2.3 (v0.4.11) and 2.2.4 (v0.4.12) already ship the fixed
openssl-libs 3.0.7-28.el9_4. The rpms.lock.yaml was updated at build v0.4.11.
Verify that the fix is correctly reflected and no regression has occurred.

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE record: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- openssl-libs is an explicitly installed RPM (confirmed present in rpms.lock.yaml)
- Update the package version spec in rpms.in.yaml / rpms.lock.yaml to >= 3.0.7-28.el9_4
- Regenerate rpms.lock.yaml if using an input spec file
- The fix is already present in builds v0.4.11+ -- verify that the current
  rpms.lock.yaml on main reflects openssl-libs >= 3.0.7-28.el9_4
- SBOM verification was skipped during triage (cosign not available); consider
  verifying the container image SBOM post-build to confirm the patched package
  is included

## Acceptance Criteria

- [ ] openssl-libs is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully

## Dependencies

- Depends on: TC-8005 (parent tracking issue)

---

## Cross-Stream Impact Comment (Case B)

The following comment would be posted to TC-8005:

```
Cross-stream impact: openssl-libs (versions before 3.0.7-28.el9_4) also
affects stream 2.1.x based on rpms.lock.yaml analysis:
  - 2.1.0 (v0.3.8): openssl-libs 3.0.7-24.el9
  - 2.1.1 (v0.3.12): openssl-libs 3.0.7-24.el9

These versions are tracked by companion issues (see Related links)
or may require separate PSIRT triage.
```

If no sibling CVE Jira exists for the 2.1.x stream, a preemptive remediation
task would be created with the `security-preemptive` label and linked to TC-8005
via "Related" link type.

## Jira Issue Creation (pseudocode)

```
task = jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (rhtpa-2.2)",
  description: <task-description-above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215"]
)

jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: <task-key>,
  type: "Depend"
)
```
