# Step 8 -- Remediation

## Triage Outcome

### Scoped Stream (2.2.x) -- Case C: Not Affected

No supported versions in the scoped stream (2.2.x) ship a vulnerable version of h2.
All versions ship h2 >= 0.4.8 which is at or above the fix threshold.

**Recommendation**: Close TC-8030 as Not a Bug (not affected).

- Resolution: Not a Bug
- VEX Justification (customfield_12345): **Component not Present** -- the vulnerable version of h2 (< 0.4.8) is not shipped in any 2.2.x version. All 2.2.x versions ship h2 0.4.8 or later, which is outside the affected range.

**Close comment**:
> No supported versions in the 2.2.x stream ship a vulnerable version of h2.
> Version impact analysis shows all 2.2.x versions ship h2 >= 0.4.8, which is
> at or above the fix threshold (0.4.8). The affected range (< 0.4.8) does not
> apply to this stream.

### Cross-Stream Impact (2.1.x) -- Case B: Proactive Remediation

The version impact analysis reveals that the **2.1.x** stream (outside TC-8030's scope)
is affected. All 2.1.x versions ship h2 0.4.5 which is below the fix threshold (0.4.8).

**Cross-stream impact comment** (to be posted on TC-8030):
> Cross-stream impact: h2 < 0.4.8 also affects stream 2.1.x based on lock file
> analysis. Stream 2.1.x ships h2 0.4.5 across all versions (2.1.0, 2.1.1).
> This stream is tracked by companion issues (see Related links) or may require
> separate PSIRT triage.

Since 2.1.x has no CVE Jira for CVE-2026-48901, create **preemptive remediation tasks**
with the `security-preemptive` label and "Related" link type.

---

## Preemptive Remediation Tasks for Stream 2.1.x

### Task 1: Upstream Backport Task (Preemptive)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Remediate CVE-2026-48901: bump h2 to 0.4.8 (2.1.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-48901", "security-preemptive"]
)
```

**Link:** Related to TC-8030 (not Depend, because this is a preemptive task from a different stream)

**Task description:**

```markdown
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for stream 2.1.x. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-48901: h2 HTTP/2 CONTINUATION flood vulnerability.
The vulnerable dependency (h2 < 0.4.8) must be updated to the fixed
version (0.4.8+).

Affected versions: 2.1.0 (h2 0.4.5, source tag v0.3.8), 2.1.1 (h2 0.4.5, source tag v0.3.12)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/hyperium/h2/pull/800
Advisory: https://github.com/advisories/GHSA-2026-r7f2-kk9p

## Implementation Notes

- Update h2 dependency to >= 0.4.8 in Cargo.lock (and Cargo.toml if pinned)
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] h2 dependency is >= 0.4.8
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8030 (originating CVE Jira, stream 2.2.x)
```

### Task 2: Downstream Propagation Subtask (Preemptive)

**Jira creation call:**
```
jira.create_issue(
  projectKey: "TC",
  issueTypeName: "Task",
  summary: "Propagate CVE-2026-48901 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)",
  description: <see below>,
  labels: ["ai-generated-jira", "Security", "CVE-2026-48901", "security-preemptive"]
)
```

**Links:**
- Related to TC-8030 (preemptive -- not Depend)
- Blocked by upstream backport task (Blocks link type)

**Task description:**

```markdown
> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8030 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for stream 2.1.x. When PSIRT creates one, this task will be linked and the
> `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-48901 fix from the upstream backport task.

The upstream backport task bumps h2 to 0.4.8 on release/0.3.z. Once that
PR merges, update the source pinning in this Konflux release repo so the
next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag, e.g., v0.3.12)
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Related to: TC-8030 (originating CVE Jira, stream 2.2.x)
```

---

## Preemptive Task Summary Comment (to be posted on TC-8030)

> Preemptive remediation tasks created for streams without CVE Jiras:
> - 2.1.x: <upstream-task-key> (upstream backport, security-preemptive),
>   <downstream-task-key> (downstream propagation, security-preemptive)
>
> These tasks use the "Related" link type and carry the security-preemptive
> label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
> reconciliation will link them and remove the label.

## Post-Triage Actions

1. **Add label**: `ai-cve-triaged` to TC-8030
2. **Close TC-8030**: Resolution "Not a Bug", VEX Justification "Component not Present" (customfield_12345)
3. **Post summary comment** on TC-8030 documenting:
   - Version impact table (2.2.x: not affected; 2.1.x: affected)
   - Affects Versions correction (if applicable)
   - Triage outcome: closed as Not a Bug for 2.2.x scope
   - Cross-stream impact: preemptive remediation tasks created for 2.1.x
   - @mention of the issue reporter
