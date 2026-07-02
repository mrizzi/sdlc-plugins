# Step 8 -- Remediation

## Triage Outcome Summary

| Stream | Affected Versions | Latest Fixed? | Remediation Action |
|--------|-------------------|---------------|-------------------|
| 2.2.x (scoped) | 2.2.0, 2.2.1, 2.2.2 | Yes (2.2.3+) | Already fixed in latest -- no new remediation task needed |
| 2.1.x (cross-stream) | 2.1.0, 2.1.1 | No | Preemptive remediation tasks required (Case B) |

## Case Analysis

### Scoped Stream (2.2.x) -- Already Fixed

The latest versions in the 2.2.x stream (2.2.3 and 2.2.4) already ship quinn-proto 0.11.14, which is the fixed version. No remediation task is needed for this stream. The Affects Versions should be corrected to RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2, and a triage summary comment should note that the fix landed in 2.2.3.

### Cross-Stream Impact (2.1.x) -- Case B: Preemptive Remediation

The 2.1.x stream is affected (all versions ship quinn-proto 0.11.9) and has no fix. Since this is outside the scoped stream, this is Case B (cross-stream impact). Preemptive remediation tasks are created with the `security-preemptive` label.

The ecosystem is **Cargo** (source dependency), so two tasks are created: an upstream backport task and a downstream propagation task.

---

## Remediation Task 1: Upstream Backport (2.1.x stream)

**Issue Type**: Task
**Summary**: CVE-2026-31812: Update quinn-proto to >= 0.11.14 in rhtpa-backend (release/0.3.z)
**Labels**: security-fix, CVE-2026-31812, security-preemptive
**Link**: Related to TC-8001 (originating CVE, scoped to 2.2.x)

### Description

#### Context

CVE-2026-31812 affects quinn-proto versions before 0.11.14. The quinn-proto crate has a denial-of-service vulnerability where a remote attacker can cause a panic by sending a QUIC transport frame that creates an excessive number of streams.

This is a **preemptive remediation task** created during triage of TC-8001 (scoped to stream 2.2.x). The 2.1.x stream does not yet have its own CVE Vulnerability issue from PSIRT.

#### Objective

Update the quinn-proto dependency to >= 0.11.14 in the rhtpa-backend repository on the `release/0.3.z` branch.

#### Current State

- **Repository**: rhtpa-backend
- **Branch**: release/0.3.z
- **Current quinn-proto version**: 0.11.9 (pinned in Cargo.lock)
- **Target version**: >= 0.11.14

#### Steps

1. Check out the `release/0.3.z` branch of rhtpa-backend
2. Update the quinn-proto dependency in `Cargo.toml` (or transitive dependency chain) to >= 0.11.14
3. Run `cargo update` to regenerate `Cargo.lock`
4. Verify the updated version: `grep -A2 'name = "quinn-proto"' Cargo.lock`
5. Run the test suite to verify no regressions
6. Create a PR targeting `release/0.3.z`

#### References

- Upstream fix PR: https://github.com/quinn-rs/quinn/pull/2048
- Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq
- CVE Record: https://www.cve.org/CVERecord?id=CVE-2026-31812
- RUSTSEC: https://rustsec.org/advisories/RUSTSEC-2026-0042.html

#### Acceptance Criteria

- [ ] quinn-proto version in Cargo.lock is >= 0.11.14
- [ ] All existing tests pass
- [ ] PR merged to release/0.3.z

---

## Remediation Task 2: Downstream Propagation (2.1.x stream)

**Issue Type**: Task (subtask, blocked by Task 1)
**Summary**: CVE-2026-31812: Propagate quinn-proto fix to rhtpa-release.0.3.z for 2.1.x
**Labels**: security-fix, CVE-2026-31812, downstream-propagation, security-preemptive
**Link**: Related to TC-8001 (originating CVE); Blocked by upstream Task 1
**Blocked By**: Upstream backport task (Task 1 above)

### Description

#### Context

This is the downstream propagation task for CVE-2026-31812 quinn-proto fix in the 2.1.x stream. It should be executed after the upstream backport task completes (the fix is merged to rhtpa-backend release/0.3.z).

This is a **preemptive remediation task** created during triage of TC-8001 (scoped to stream 2.2.x).

#### Objective

Update the backend source reference in the rhtpa-release.0.3.z Konflux release repository to point to the new backend tag that includes the quinn-proto fix.

#### Current State

- **Konflux release repo**: rhtpa-release.0.3.z
- **Source pinning file**: artifacts.lock.yaml
- **Current backend tag**: v0.3.12 (quinn-proto 0.11.9 -- vulnerable)
- **Target**: New backend tag from release/0.3.z with quinn-proto >= 0.11.14

#### Steps

1. Wait for the upstream backport task to complete and a new backend tag to be created on release/0.3.z
2. Update `artifacts.lock.yaml` in rhtpa-release.0.3.z to reference the new backend tag
3. Verify the new tag contains the fixed quinn-proto version: `git show <new-tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
4. Create a PR in the rhtpa-release.0.3.z repository
5. Trigger a new build for the 2.1.x stream

#### References

- Upstream fix PR: https://github.com/quinn-rs/quinn/pull/2048
- Advisory: https://github.com/advisories/GHSA-2026-qp73-x4mq

#### Acceptance Criteria

- [ ] artifacts.lock.yaml updated with new backend tag
- [ ] New tag confirmed to contain quinn-proto >= 0.11.14
- [ ] Build triggered and completes successfully for 2.1.x stream

---

## Cross-Stream Impact Comment (to post on TC-8001)

```
Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis.
All 2.1.x versions (2.1.0, 2.1.1) ship quinn-proto 0.11.9 which is within the affected range.
Stream 2.1.x does not currently have a companion CVE Vulnerability issue.

Preemptive remediation tasks created for streams without CVE Jiras:
- 2.1.x: <upstream-task-key> (security-preemptive, upstream backport)
- 2.1.x: <downstream-task-key> (security-preemptive, downstream propagation)

These tasks use the "Related" link type and carry the security-preemptive label.
When PSIRT creates stream-specific CVE Jiras, Step 4.4 reconciliation will link
them and remove the label.
```

## Post-Triage Actions

1. Add `ai-cve-triaged` label to TC-8001
2. Correct Affects Versions: remove RHTPA 2.0.0, add RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
3. Post triage summary comment noting:
   - Fix already present in 2.2.3+ (quinn-proto 0.11.14)
   - Cross-stream impact on 2.1.x
   - Preemptive remediation tasks created for 2.1.x
4. @mention the issue reporter in the summary comment
