# Step 8 -- Remediation

## Triage Outcome

TC-8020 is scoped to stream rhtpa-2.2. The version impact analysis shows:

- **rhtpa-2.2 stream**: RHTPA 2.2.0 and 2.2.1 are affected (tokio 1.41.1 < 1.42.0) -- **Case A**
- **rhtpa-2.1 stream**: RHTPA 2.1.0 and 2.1.1 are affected (tokio 1.40.0 < 1.42.0), but no CVE Jira exists for this stream -- **Case B**

---

## Case A: Remediation Tasks for Current Stream (rhtpa-2.2)

Since tokio is a Cargo (source dependency) ecosystem, two tasks are created for the rhtpa-2.2 stream.

### Task 1: Upstream Backport Task

**Summary**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`

**Description**:

> ## Repository
>
> backend
>
> ## Target Branch
>
> release/0.4.z
>
> ## Description
>
> Remediate CVE-2026-55123: use-after-free in task abort in the tokio crate.
> The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed
> version (1.42.0+).
>
> Affected versions: RHTPA 2.2.0 (tokio 1.41.1), RHTPA 2.2.1 (tokio 1.41.1)
>
> Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
> Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp
>
> ## Implementation Notes
>
> - Update tokio dependency to >= 1.42.0 in Cargo.lock
> - Target branch: release/0.4.z
> - Check for pinned versions or transitive dependency constraints
>   that might prevent the bump
> - If a direct bump introduces breaking changes, assess whether a
>   code-level workaround is viable (see upstream changelog)
>
> ### Coordination Guidance
>
> This component is public upstream. Coordinate fix with upstream maintainers
> if the vulnerability is not yet public. Follow your organization's embargo
> policy before discussing in public channels or PRs.
>
> ## Acceptance Criteria
>
> - [ ] tokio dependency is >= 1.42.0
> - [ ] No other dependency conflicts introduced
> - [ ] Existing tests pass
>
> ## Test Requirements
>
> - [ ] Existing test suite passes with the updated dependency
>
> ## Dependencies
>
> - Depends on: TC-8020 (parent tracking issue)

**Linkage**: Depend link from TC-8020 to this task

---

### Task 2: Downstream Propagation Subtask

**Summary**: Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`

**Description**:

> ## Repository
>
> rhtpa-release.0.4.z
>
> ## Target Branch
>
> main
>
> ## Description
>
> Update backend reference in rhtpa-release.0.4.z to pick up the
> CVE-2026-55123 fix from the upstream backport task.
>
> The upstream backport bumps tokio to 1.42.0 on release/0.4.z. Once that PR
> merges, update the source pinning in this Konflux release repo so the next
> build ships the fix.
>
> ## Implementation Notes
>
> - Source pinning method: artifacts.lock.yaml (download URL contains tag)
> - Update the backend reference to the merged commit or new release tag
> - Verify the Konflux build pipeline triggers successfully
>
> ## Acceptance Criteria
>
> - [ ] backend reference updated to include the fix
> - [ ] Konflux rebuild triggers new container image
>
> ## Test Requirements
>
> - [ ] Container image builds successfully with the updated reference
>
> ## Dependencies
>
> - Depends on: upstream backport task (upstream backport must merge first)
> - Depends on: TC-8020 (parent tracking issue)

**Linkage**:
- Blocks link: upstream task blocks this downstream task
- Depend link from TC-8020 to this task

---

## Case B: Preemptive Remediation Tasks for Stream rhtpa-2.1

Stream rhtpa-2.1 is also affected (tokio 1.40.0 < 1.42.0) but has no CVE Jira. Preemptive remediation tasks are created per the Preemptive Task Variant template.

### Preemptive Task 1: Upstream Backport Task (rhtpa-2.1)

**Summary**: Remediate CVE-2026-55123: bump tokio to 1.42.0 (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2). No stream-specific CVE Jira
> exists yet for this stream. When PSIRT creates one, this task will be linked
> and the `security-preemptive` label removed.
>
> ## Repository
>
> backend
>
> ## Target Branch
>
> release/0.3.z
>
> ## Description
>
> Remediate CVE-2026-55123: use-after-free in task abort in the tokio crate.
> The vulnerable dependency (tokio < 1.42.0) must be updated to the fixed
> version (1.42.0+).
>
> Affected versions: RHTPA 2.1.0 (tokio 1.40.0), RHTPA 2.1.1 (tokio 1.40.0)
>
> Upstream fix: https://github.com/tokio-rs/tokio/pull/7001
> Advisory: https://github.com/advisories/GHSA-2026-tk91-v5pp
>
> ## Implementation Notes
>
> - Update tokio dependency to >= 1.42.0 in Cargo.lock
> - Target branch: release/0.3.z
> - Check for pinned versions or transitive dependency constraints
>   that might prevent the bump
> - If a direct bump introduces breaking changes, assess whether a
>   code-level workaround is viable (see upstream changelog)
>
> ### Coordination Guidance
>
> This component is public upstream. Coordinate fix with upstream maintainers
> if the vulnerability is not yet public. Follow your organization's embargo
> policy before discussing in public channels or PRs.
>
> ## Acceptance Criteria
>
> - [ ] tokio dependency is >= 1.42.0
> - [ ] No other dependency conflicts introduced
> - [ ] Existing tests pass
>
> ## Test Requirements
>
> - [ ] Existing test suite passes with the updated dependency
>
> ## Dependencies
>
> - Depends on: TC-8020 (originating CVE, cross-stream)

**Linkage**: Related link (not Depend) from TC-8020 to this preemptive task

---

### Preemptive Task 2: Downstream Propagation Subtask (rhtpa-2.1)

**Summary**: Propagate CVE-2026-55123 fix: update backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-55123`, `security-preemptive`

**Description**:

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8020 (stream rhtpa-2.2). No stream-specific CVE Jira
> exists yet for this stream. When PSIRT creates one, this task will be linked
> and the `security-preemptive` label removed.
>
> ## Repository
>
> rhtpa-release.0.3.z
>
> ## Target Branch
>
> main
>
> ## Description
>
> Update backend reference in rhtpa-release.0.3.z to pick up the
> CVE-2026-55123 fix from the upstream backport preemptive task.
>
> The upstream backport bumps tokio to 1.42.0 on release/0.3.z. Once that PR
> merges, update the source pinning in this Konflux release repo so the next
> build ships the fix.
>
> ## Implementation Notes
>
> - Source pinning method: artifacts.lock.yaml (download URL contains tag)
> - Update the backend reference to the merged commit or new release tag
> - Verify the Konflux build pipeline triggers successfully
>
> ## Acceptance Criteria
>
> - [ ] backend reference updated to include the fix
> - [ ] Konflux rebuild triggers new container image
>
> ## Test Requirements
>
> - [ ] Container image builds successfully with the updated reference
>
> ## Dependencies
>
> - Depends on: upstream backport preemptive task (upstream backport must merge first)
> - Depends on: TC-8020 (originating CVE, cross-stream)

**Linkage**:
- Related link (not Depend) from TC-8020 to this preemptive task
- Blocks link: preemptive upstream task blocks this preemptive downstream task

---

## Post-Triage Actions

1. Add label `ai-cve-triaged` to TC-8020
2. Post summary comment to TC-8020 documenting:
   - Version impact table
   - Affects Versions correction (if any)
   - Remediation tasks created (Case A: rhtpa-2.2 upstream + downstream)
   - Preemptive tasks created (Case B: rhtpa-2.1 upstream + downstream)
   - @mention of the issue reporter
3. Comment footnote: "This comment was AI-generated by [sdlc-workflow/triage-security](https://github.com/mrizzi/sdlc-plugins) v0.11.1."
