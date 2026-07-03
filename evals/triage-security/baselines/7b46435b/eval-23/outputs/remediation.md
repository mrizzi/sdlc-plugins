# Step 8 -- Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome

### 2.2.x stream (scoped stream -- Case A with already-fixed outcome)

The issue is scoped to stream 2.2.x. Versions 2.2.0, 2.2.1, and 2.2.2 are
affected, but versions 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14
(the fixed version). The upstream branch `release/0.4.z` also carries the fix.

**No remediation task needed for 2.2.x.** The fix was already incorporated
starting with version 2.2.3 (build 0.4.11, backend tag v0.4.11).

Affects Versions correction: `RHTPA 2.0.0` -> `RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2`

### 2.1.x stream (cross-stream impact -- Case B)

Cross-stream impact detected: the 2.1.x stream is also affected. All versions
(2.1.0, 2.1.1) ship quinn-proto 0.11.9, which is within the vulnerable range.
The upstream branch `release/0.3.z` still carries the vulnerable version.

No CVE Jira exists for the 2.1.x stream. Preemptive remediation tasks are
created below.

---

## Preemptive Remediation Tasks (2.1.x stream)

These tasks carry the `security-preemptive` label and use the "Related" link
type to the originating CVE Jira TC-8001 (stream 2.2.x). When PSIRT creates
a stream-specific CVE Jira for 2.1.x, Step 4.4 reconciliation will link them
and remove the `security-preemptive` label.

### Task 1: Upstream Backport (source repo fix)

**Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link:** Related to TC-8001

#### Task Description

## Repository

backend

## Target Branch

release/0.3.z

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

Remediate CVE-2026-31812: quinn-proto panic on large stream counts (DoS).
The vulnerable dependency (quinn-proto < 0.11.14) must be updated to the
fixed version (0.11.14+).

Affected versions: RHTPA 2.1.0 (v0.3.8, quinn-proto 0.11.9), RHTPA 2.1.1 (v0.3.12, quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Update quinn-proto dependency to >= 0.11.14 in Cargo.lock
- Target branch: release/0.3.z
- Check for pinned versions or transitive dependency constraints
  that might prevent the bump
- If a direct bump introduces breaking changes, assess whether a
  code-level workaround is viable (see upstream changelog)

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for
CVE assignment, advisory preparation, and formal disclosure. Fix must be released
via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] quinn-proto dependency is >= 0.11.14
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Related to: TC-8001 (originating CVE Jira, stream 2.2.x)

---

### Task 2: Downstream Propagation (Konflux release repo update)

**Summary:** Propagate CVE-2026-31812 fix: update backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link:** Related to TC-8001; Blocked by Task 1 (upstream backport)

#### Task Description

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x). No stream-specific CVE Jira exists
> yet for the 2.1.x stream. When PSIRT creates one, this task will be linked and
> the `security-preemptive` label removed.

Update backend reference in rhtpa-release.0.3.z to pick up the CVE-2026-31812
fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14 on release/0.3.z. Once that
PR merges, update the source pinning in this Konflux release repo so the next
build ships the fix.

## Implementation Notes

- Source pinning method: `artifacts.lock.yaml` (download URL contains tag, e.g., `v0.3.12`)
- Update the backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

### Coordination Guidance

This component is shipped to customers. Coordinate with Product Security for
CVE assignment, advisory preparation, and formal disclosure. Fix must be released
via a security advisory with explicit CVE-to-component mapping.

## Acceptance Criteria

- [ ] backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Blocked by: Task 1 (upstream backport must merge first)
- Related to: TC-8001 (originating CVE Jira, stream 2.2.x)

---

## Cross-Stream Impact Comment (for TC-8001)

The following comment would be posted to TC-8001:

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on
lock file analysis. Stream 2.1.x has no CVE Jira yet.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: [upstream-task-key] (upstream backport, security-preemptive)
- 2.1.x: [downstream-task-key] (downstream propagation, security-preemptive)

These tasks use the "Related" link type and carry the security-preemptive label.
When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link
them and remove the label.
```

## Coordination Guidance Reference

The deployment context for rhtpa-backend is **customer-shipped**, sourced from
the Source Repositories table in the project CLAUDE.md Security Configuration:

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | customer-shipped |

Per the remediation-templates.md Coordination Guidance section, the
`customer-shipped` deployment context produces the following guidance appended
to the Implementation Notes of each remediation task:

> **Coordination Guidance**: This component is shipped to customers. Coordinate
> with Product Security for CVE assignment, advisory preparation, and formal
> disclosure. Fix must be released via a security advisory with explicit
> CVE-to-component mapping.

This guidance is included in both the upstream backport task and the downstream
propagation task above.
