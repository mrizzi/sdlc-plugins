# Step 8 — Remediation: CVE-2026-48901

## Triage Decision

### Scoped Stream (2.2.x) — Close as Not a Bug

The issue TC-8030 is scoped to stream 2.2.x. No versions in the 2.2.x stream are
affected: all versions ship h2 >= 0.4.8, which is at or above the fix threshold.

**Recommendation**: Close TC-8030 as Not a Bug (not affected).

**Proposed actions**:
1. Add comment documenting the version impact analysis and non-affected status
2. Transition to Closed with resolution "Not a Bug"
3. Set VEX Justification (customfield_12345) to "Component not Present" — the
   vulnerable version of h2 (< 0.4.8) is not shipped in any 2.2.x version

### Cross-Stream Impact (Case B) — Preemptive Remediation for 2.1.x

The version impact analysis reveals that stream 2.1.x (outside this issue's scope)
IS affected: versions 2.1.0 and 2.1.1 both ship h2 0.4.5 (< 0.4.8).

**Cross-stream impact comment** (to post on TC-8030):

> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file
> analysis. Versions 2.1.0 and 2.1.1 ship h2 0.4.5. These streams are tracked by
> companion issues (see Related links) or may require separate PSIRT triage.

Since this is a source dependency ecosystem (Cargo), preemptive remediation creates
**two tasks** per affected stream: an upstream backport task and a downstream
propagation subtask.

---

## Preemptive Remediation Tasks for Stream 2.1.x

Labels for preemptive tasks: `["ai-generated-jira", "Security", "CVE-2026-48901", "security-preemptive"]`
Link type to originating CVE (TC-8030): **Related** (not Depend)

### Task 1: Upstream Backport (2.1.x)

**Summary**: Remediate CVE-2026-48901: bump h2 to 0.4.8 (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-48901, security-preemptive

```markdown
## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for stream 2.1.x. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed version (0.4.8+).

Affected versions: 2.1.0 (h2 0.4.5 at v0.3.8), 2.1.1 (h2 0.4.5 at v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: check Cargo.lock to determine if h2 is direct or transitive

### Remediation approach (direct dependency)

When h2 is a **direct** dependency of a workspace member:

- Update h2 dependency to >= 0.4.8 in Cargo.toml
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Remediation approach (transitive dependency)

When h2 is a **transitive** dependency (pulled in through intermediate packages),
use a two-tier approach:

**Preferred: bump the direct dependency**
- Identify the direct dependency that pulls in h2 (see dependency chain)
- Bump the direct dependency to a version whose transitive closure
  includes h2 >= 0.4.8
- Verify the bump does not introduce breaking API changes to the
  direct dependency

**Fallback: pin the transitive dependency directly**
If bumping the direct dependency is not viable:
- `cargo add h2@0.4.8` to add as a direct dependency, overriding the
  transitive resolution
- Document why the direct dep bump was not viable in the PR description

### Coordination Guidance

This component is public upstream. Coordinate fix with upstream maintainers
if the vulnerability is not yet public. Follow your organization's embargo policy
before discussing in public channels or PRs.

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8030 (originating CVE Jira, stream 2.2.x)
```

### Task 2: Downstream Propagation (2.1.x)

**Summary**: Propagate CVE-2026-48901 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (rhtpa-2.1)

**Labels**: ai-generated-jira, Security, CVE-2026-48901, security-preemptive

```markdown
## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for stream 2.1.x. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-48901 fix from the upstream backport task.

The upstream backport bumps h2 to 0.4.8 on release/0.3.z. Once that PR merges,
update the source pinning in this Konflux release repo so the next build ships
the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Blocked by: upstream backport task (upstream backport must merge first)
- Related to: TC-8030 (originating CVE Jira, stream 2.2.x)
```

## Jira Linkage for Preemptive Tasks

After creating the preemptive tasks:

1. Link upstream backport task to TC-8030 with type **Related** (preemptive, not Depend)
2. Link downstream propagation subtask to TC-8030 with type **Related** (preemptive)
3. Link downstream propagation subtask as **blocked by** upstream backport task (type: Blocks)

## Post-Triage Comment on TC-8030

```
Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: [upstream-task-key] (upstream backport, security-preemptive)
- 2.1.x: [downstream-task-key] (downstream propagation, security-preemptive, blocked by upstream)

These tasks use the "Related" link type and carry the security-preemptive
label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
reconciliation will link them and remove the label.
```

## Close Recommendation for TC-8030

Post comment on TC-8030:

> No supported versions in stream 2.2.x ship a vulnerable version of h2.
> Version impact analysis: all 2.2.x versions (2.2.0 through 2.2.4) ship h2 >= 0.4.8,
> which is outside the affected range (< 0.4.8).
>
> Cross-stream impact: stream 2.1.x is affected (h2 0.4.5 < 0.4.8).
> Preemptive remediation tasks created for 2.1.x.
>
> Closing this issue as Not a Bug for stream 2.2.x.

Actions:
1. Transition TC-8030 to Closed with resolution "Not a Bug"
2. Set VEX Justification (customfield_12345) to "Component not Present"
3. Add label `ai-cve-triaged`
