# Step 8 -- Remediation: TC-8001 (CVE-2026-31812)

## Triage Outcome

- **Case A**: Stream 2.2.x (scoped) -- versions 2.2.0, 2.2.1, 2.2.2 are affected
- **Case B**: Stream 2.1.x (cross-stream) -- versions 2.1.0, 2.1.1 are affected; no sibling CVE Jira exists for 2.1.x, so preemptive remediation tasks are created

Ecosystem: **Cargo** (source dependency) -- two tasks per stream: upstream backport + downstream propagation.

---

## Case A: Remediation Tasks for Stream 2.2.x (Scoped)

### Task 1: Upstream Backport (2.2.x)

**Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.2.x)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Link:** Depend -- inward: TC-8001, outward: this task

#### Task Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.2.0 (quinn-proto 0.11.9), 2.2.1 (quinn-proto 0.11.12), 2.2.2 (retag of 2.2.1)
Source commit(s): v0.4.5, v0.4.8

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct (backend workspace -> quinn-proto)

### Remediation approach (direct dependency)

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

### Task 2: Downstream Propagation (2.2.x)

**Summary:** Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (2.2.x)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`

**Links:**
- Depend -- inward: TC-8001, outward: this task
- Blocks -- inward: upstream task (Task 1), outward: this task

#### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.4.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Case B: Preemptive Remediation Tasks for Stream 2.1.x (Cross-Stream)

These tasks are created proactively because stream 2.1.x is also affected but has
no stream-specific CVE Jira. They carry the `security-preemptive` label and use
"Related" link type to the originating CVE Jira (TC-8001).

### Task 3: Upstream Backport (2.1.x, Preemptive)

**Summary:** Remediate CVE-2026-31812: bump quinn-proto to 0.11.14 (2.1.x)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Link:** Related -- inward: TC-8001, outward: this task

#### Task Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

rhtpa-backend

## Target Branch

release/0.3.z

## Description

Remediate CVE-2026-31812: quinn-proto panic on large stream counts.
The vulnerable dependency (quinn-proto < 0.11.14) must be updated
to the fixed version (0.11.14+).

Affected versions: 2.1.0 (quinn-proto 0.11.9), 2.1.1 (quinn-proto 0.11.9)
Source commit(s): v0.3.8, v0.3.12

Upstream fix: https://github.com/quinn-rs/quinn/pull/2048
Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

## Implementation Notes

- Target branch: release/0.3.z
- **Dependency type**: direct (backend workspace -> quinn-proto)

### Remediation approach (direct dependency)

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

### Task 4: Downstream Propagation (2.1.x, Preemptive)

**Summary:** Propagate CVE-2026-31812 fix: update rhtpa-backend ref in rhtpa-release.0.3.z (2.1.x)

**Labels:** `ai-generated-jira`, `Security`, `CVE-2026-31812`, `security-preemptive`

**Links:**
- Related -- inward: TC-8001, outward: this task
- Blocks -- inward: upstream task (Task 3), outward: this task

#### Task Description

> **Preemptive remediation**: This task was created proactively from cross-stream
> impact analysis of TC-8001 (stream 2.2.x).
> No stream-specific CVE Jira exists yet for this stream. When PSIRT creates one,
> this task will be linked and the `security-preemptive` label removed.

## Repository

rhtpa-release.0.3.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.3.z to pick up the
CVE-2026-31812 fix from the upstream backport task.

The upstream backport bumps quinn-proto to 0.11.14
on release/0.3.z. Once that PR merges, update the source pinning in this
Konflux release repo so the next build ships the fix.

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct -- carried forward from upstream task
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8001 (parent tracking issue)

---

## Post-Triage Summary

### Triage Actions Performed

1. **Data Extraction (Step 1):** Parsed CVE-2026-31812 data -- quinn-proto < 0.11.14, Cargo ecosystem, scoped to stream 2.2.x
2. **Version Impact Analysis (Step 2):** 5 of 7 versions across 2 streams are affected (2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2)
3. **Affects Versions Correction (Step 3):** RHTPA 2.0.0 (wrong) -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
4. **Cross-Stream Impact (Case B):** Stream 2.1.x also affected -- preemptive remediation tasks created
5. **Remediation (Case A + B):** 4 tasks total:
   - 2.2.x upstream backport (Task 1)
   - 2.2.x downstream propagation (Task 2, blocked by Task 1)
   - 2.1.x upstream backport, preemptive (Task 3)
   - 2.1.x downstream propagation, preemptive (Task 4, blocked by Task 3)

### Labels Added to TC-8001

- `ai-cve-triaged`
