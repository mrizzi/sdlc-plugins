# Step 7: Remediation Tasks

## Ecosystem: Cargo

For Cargo ecosystem vulnerabilities, two remediation tasks are required:

1. **Upstream backport task** -- Update the dependency in the source repository
2. **Downstream propagation subtask** -- Propagate the updated dependency to the release repository

The downstream task has a **Blocks** dependency on the upstream task (downstream blocks resolution of the upstream task until propagation is complete).

---

## Task 1: Upstream Backport

**Issue Type**: Task (subtask of TC-8001)

**Summary**: Update quinn-proto to >= 0.11.14 in rhtpa-backend (release/0.4.z)

### Repository

rhtpa-backend (https://github.com/rhtpa/rhtpa-backend)

### Target Branch

`release/0.4.z`

### Description

Update the quinn-proto dependency in rhtpa-backend to version 0.11.14 or later to remediate CVE-2026-31812. The vulnerability allows a remote attacker to cause a denial of service (DoS) by sending a QUIC transport frame that creates an excessive number of streams, leading to a panic.

### Implementation Notes

- The upstream fix is available in quinn-proto 0.11.14 (see [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048))
- Update `Cargo.toml` to require quinn-proto >= 0.11.14
- Run `cargo update -p quinn-proto` to update `Cargo.lock`
- Verify no breaking API changes between 0.11.12 and 0.11.14
- The fix was already picked up in build tag `v0.4.11` (RHTPA 2.2.3), so the `release/0.4.z` branch HEAD may already contain the fix; verify before creating a PR

### Acceptance Criteria

- [ ] quinn-proto version in `Cargo.lock` on `release/0.4.z` is >= 0.11.14
- [ ] All existing tests pass with the updated dependency
- [ ] No regressions in QUIC connectivity functionality

### Dependencies

None (this is the upstream task)

---

## Task 2: Downstream Propagation

**Issue Type**: Task (subtask of TC-8001)
**Dependency**: Blocks Task 1 (upstream backport)

**Summary**: Propagate quinn-proto fix to rhtpa-release.0.4.z

### Repository

rhtpa-release.0.4.z (git.example.com/rhtpa/rhtpa-release.0.4.z)

### Target Branch

Main branch of the release repository

### Description

After the upstream backport of quinn-proto >= 0.11.14 lands in rhtpa-backend `release/0.4.z`, update the backend component pin in the Konflux release repository to reference a build that includes the fix. This ensures new product builds ship the remediated dependency.

### Implementation Notes

- Wait for the upstream backport (Task 1) to merge and a new backend build to be produced
- Update `artifacts.lock.yaml` in rhtpa-release.0.4.z to reference the new backend build tag that includes quinn-proto >= 0.11.14
- The fix is already present in builds from tag `v0.4.11` onward; if the release repo already points to `v0.4.11` or later, this task may already be satisfied
- Verify the updated build tag's `Cargo.lock` contains quinn-proto >= 0.11.14

### Acceptance Criteria

- [ ] `artifacts.lock.yaml` references a backend build containing quinn-proto >= 0.11.14
- [ ] A new product build can be produced from the updated release repository
- [ ] The vulnerability is no longer detected in the new product build

### Dependencies

- Blocks: Task 1 (Upstream Backport -- Update quinn-proto to >= 0.11.14 in rhtpa-backend)
