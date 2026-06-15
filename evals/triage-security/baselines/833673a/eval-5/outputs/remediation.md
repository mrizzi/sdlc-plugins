# Step 7 — Remediation

## Triage Outcome

**Case A: Affected — create remediation task.**

Within the 2.2.x stream scope, versions 2.2.0, 2.2.1, and 2.2.2 ship a vulnerable
version of openssl-libs (< 3.0.7-28.el9_4). Versions 2.2.3 and 2.2.4 already ship
the fixed version (3.0.7-28.el9_4).

**Ecosystem**: RPM (system package) — only **one** remediation task is needed.
No upstream backport task required since the fix is an RPM update in the Konflux
release repo.

## Cross-stream Impact Notice (Case B)

The 2.1.x stream is also affected (versions 2.1.0 and 2.1.1 ship openssl-libs
3.0.7-24.el9). This is tracked by a companion Vulnerability issue scoped to that
stream. A comment would be posted to TC-8005 noting the cross-stream impact.

## Remediation Task Description

**Summary**: Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)

**Labels**: ai-generated-jira, Security, CVE-2026-40215

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Remediate CVE-2026-40215: update openssl-libs to >= 3.0.7-28.el9_4 in the
Konflux release repo for the 2.2.x stream.

A buffer over-read vulnerability in openssl-libs (CVE-2026-40215, CVSS 7.1 High)
affects X.509 certificate chain verification. Versions before 3.0.7-28.el9_4 are
vulnerable. The fix is available in RHSA-2026:4021.

Affected product versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Already fixed in: RHTPA 2.2.3+ (ships 3.0.7-28.el9_4)

Note: Since the fix is already present in versions 2.2.3 and 2.2.4, this
remediation applies only to rebuild/respin scenarios for older releases in the
stream. The rpms.lock.yaml already contains 3.0.7-28.el9_4 at the latest pinned
commits (v0.4.11, v0.4.12).

Advisory: https://access.redhat.com/errata/RHSA-2026:4021
CVE: https://www.cve.org/CVERecord?id=CVE-2026-40215

## Implementation Notes

- The openssl-libs package is pinned in `rpms.lock.yaml`
- Update the openssl-libs entry to >= 3.0.7-28.el9_4
- If using rpms.in.yaml, update the package spec there and regenerate rpms.lock.yaml
- The patched RPM is available via RHSA-2026:4021
- Verify the Konflux build pipeline triggers successfully after the update

## Acceptance Criteria

- [ ] openssl-libs version in rpms.lock.yaml is >= 3.0.7-28.el9_4
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated openssl-libs

## Dependencies

- Depends on: TC-8005 (parent Vulnerability tracking issue)

---

## Jira Creation Call (would execute after engineer confirmation)

```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-40215: update openssl-libs to 3.0.7-28.el9_4 (2.2.x)",
  description: <task-description-above>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-40215"]
)
```

## Jira Linkage (would execute after task creation)

```
jira.create_link(
  inwardIssue: "TC-8005",
  outwardIssue: "<new-task-key>",
  type: "Depend"
)
```

## Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8005
2. Post summary comment to TC-8005 with:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 -> RHTPA 2.2.0, 2.2.1, 2.2.2)
   - Remediation task link
   - Cross-stream impact notice (2.1.x also affected)
3. Transition TC-8005 to In Progress
4. Assign TC-8005 to current user
