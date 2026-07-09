# Remediation -- CVE-2026-31812 (quinn-proto < 0.11.14)

## Triage Decision

### Stream 2.2.x (in-scope)

The fix for CVE-2026-31812 already landed in the 2.2.x stream starting with version
2.2.3 (quinn-proto bumped to 0.11.14 at tag v0.4.11). Versions 2.2.3 and 2.2.4
ship the fixed version. No remediation tasks are needed for the 2.2.x stream.

**Action**: Correct Affects Versions to RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2.
Add comment noting the fix is already present in 2.2.3+.

### Stream 2.1.x (cross-stream, Case B)

All versions in the 2.1.x stream (2.1.0 and 2.1.1) ship quinn-proto 0.11.9, which
is within the affected range (< 0.11.14). The upstream branch release/0.3.z does not
have the fix. No stream-specific CVE Jira exists for 2.1.x.

**Action**: Create preemptive remediation tasks for the 2.1.x stream (Case B).
Since quinn-proto is a Cargo (source dependency) ecosystem, two tasks are created:
an upstream backport task and a downstream propagation subtask.

---

## Cross-Stream Impact Comment (posted to TC-8001)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on
lock file analysis. All versions in stream 2.1.x (2.1.0, 2.1.1) ship quinn-proto
0.11.9. This stream does not have a companion CVE Jira -- preemptive remediation
tasks have been created below.
```

---

## Task 1: Upstream Backport (2.1.x stream, preemptive)

**Summary**: Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link**: Related to TC-8001 (originating CVE, different stream)

### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

## Repository

backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (v0.3.8, quinn-proto 0.11.9), 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct

### Remediation approach (direct dependency)

When the vulnerable package is a **direct** dependency of a workspace member:

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8001 (parent tracking issue)

---

## Task 2: Downstream Propagation (2.1.x stream, preemptive)

**Summary**: Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link**: Related to TC-8001 (originating CVE, different stream)

**Blocked by**: Task 1 (upstream backport must merge first)

### Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- **Dependency type**: direct -- carried forward from upstream task
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: Task 1 (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Post-Triage Actions

### Jira Mutations (require engineer confirmation)

1. **Affects Versions correction on TC-8001**:
   - Remove: RHTPA 2.0.0
   - Add: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

2. **Create upstream backport task** (Task 1):
   - Summary: "Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)"
   - Labels: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
   - Link: Related to TC-8001

3. **Create downstream propagation task** (Task 2):
   - Summary: "Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)"
   - Labels: ai-generated-jira, Security, CVE-2026-31812, security-preemptive
   - Link: Related to TC-8001
   - Blocked by: Task 1

4. **Post cross-stream impact comment** on TC-8001

5. **Post preemptive task comment** on TC-8001:
   ```
   Preemptive remediation tasks created for streams without CVE Jiras:
   - 2.1.x: [upstream-task-key] (upstream backport, security-preemptive)
   - 2.1.x: [downstream-task-key] (downstream propagation, security-preemptive)

   These tasks use the "Related" link type and carry the security-preemptive
   label. When PSIRT creates stream-specific CVE Jiras, Step 4.4
   reconciliation will link them and remove the label.
   ```

6. **Add `ai-cve-triaged` label** to TC-8001

7. **Post triage summary comment** on TC-8001 with:
   - Version impact table
   - Affects Versions correction (RHTPA 2.0.0 removed, RHTPA 2.2.0/2.2.1/2.2.2 added)
   - Note that 2.2.x is already fixed in 2.2.3+
   - Links to preemptive remediation tasks for 2.1.x
   - @mention of the issue reporter
