# Step 8 -- Remediation

## Triage Decision: Case C -- No supported versions affected (in scoped stream)

The version impact analysis shows that **no versions in the 2.2.x stream** (the scoped stream for TC-8030) ship a vulnerable version of h2. All five 2.2.x versions (2.2.0 through 2.2.4) ship h2 >= 0.4.8, which is at or above the fix threshold.

### Recommended Action: Close TC-8030 as Not a Bug

**Rationale**: No supported versions in the 2.2.x stream ship a vulnerable version of h2. Version impact analysis confirms all 2.2.x versions include h2 0.4.8 or later, which is outside the affected range (< 0.4.8).

**Jira Actions (pending engineer confirmation):**

1. Add comment to TC-8030:

   > No supported versions in the 2.2.x stream ship a vulnerable version of h2.
   > Version impact analysis:
   >
   > | Version | h2 version | Affected? |
   > |---------|------------|-----------|
   > | 2.2.0 | 0.4.8 | NO |
   > | 2.2.1 | 0.4.8 | NO |
   > | 2.2.2 | 0.4.8 | NO (retag of 2.2.1) |
   > | 2.2.3 | 0.4.9 | NO |
   > | 2.2.4 | 0.4.9 | NO |
   >
   > All supported versions ship h2 >= 0.4.8, which is outside the affected range (< 0.4.8).
   > Fix threshold source: MITRE CVE API and OSV.dev (cross-validated, in agreement).
   >
   > Cross-stream impact: 2.1.x stream versions (2.1.0, 2.1.1) ship h2 0.4.5, which IS affected. The 2.1.x stream is tracked separately and may require its own CVE Jira from PSIRT.

2. Transition TC-8030 to **Closed** with resolution **Not a Bug**.

3. Set VEX Justification (customfield_12345) to **Component not Present** -- the vulnerable version of h2 (< 0.4.8) is not present in any 2.2.x version.

4. Add label `ai-cve-triaged` to TC-8030.

## Cross-Stream Impact Notice (2.1.x)

Although TC-8030 (scoped to 2.2.x) should be closed, the 2.1.x stream IS affected:

| Version | h2 version | Affected? |
|---------|------------|-----------|
| 2.1.0 | 0.4.5 | YES |
| 2.1.1 | 0.4.5 | YES |

### Preemptive Remediation Tasks for 2.1.x

Since TC-8030 is scoped to 2.2.x and the 2.1.x stream does not have its own CVE Jira for this vulnerability, create preemptive remediation tasks for 2.1.x per Case B.

#### Task 1: Upstream Backport (2.1.x stream)

```
Summary: Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.1.x)
Labels: ai-generated-jira, Security, CVE-2026-48901, security-preemptive
Link: Related to TC-8030
```

**Task Description:**

## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for the 2.1.x stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: 2.1.0 (backend v0.3.8, h2 0.4.5), 2.1.1 (backend v0.3.12, h2 0.4.5)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: requires lock file inspection for full chain determination
- Update h2 dependency to >= 0.4.8 in Cargo.lock / Cargo.toml

### Remediation approach

- Update h2 to >= 0.4.8 in the workspace dependencies
- If h2 is a transitive dependency, bump the direct dependency that pulls it in to a version whose transitive closure includes h2 >= 0.4.8
- Verify the bump does not introduce breaking API changes

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8030 (originating CVE Jira, stream 2.2.x)

---

#### Task 2: Downstream Propagation (2.1.x stream)

```
Summary: Propagate CVE-2026-48901 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)
Labels: ai-generated-jira, Security, CVE-2026-48901, security-preemptive
Link: Related to TC-8030, Blocked by upstream backport task
```

**Task Description:**

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for the 2.1.x stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-48901 fix from the upstream backport task.

The upstream backport bumps h2 to >= 0.4.8 on release/0.3.z. Once that PR merges, update the source pinning in this Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Blocked by: upstream backport task (upstream backport must merge first)
- Related to: TC-8030 (originating CVE Jira, stream 2.2.x)

---

### Post-Triage Comment on TC-8030

After task creation, post a comment on TC-8030:

> Preemptive remediation tasks created for streams without CVE Jiras:
> - 2.1.x: [upstream-task-key] (security-preemptive, upstream backport)
> - 2.1.x: [downstream-task-key] (security-preemptive, downstream propagation)
>
> These tasks use the "Related" link type and carry the security-preemptive
> label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
> reconciliation will link them and remove the label.
