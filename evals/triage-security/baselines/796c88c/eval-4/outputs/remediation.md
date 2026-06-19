# Remediation Tasks — TC-8004

## Stream Applicability

| Stream | Affected? | Remediation Needed? |
|--------|-----------|---------------------|
| **2.1.x** | YES | **YES** — h2 0.4.5 must be updated to >= 0.4.8 |
| **2.2.x** | NO | **NO** — already ships h2 >= 0.4.8 |

Remediation tasks are created **only** for the 2.1.x stream.

Since the issue is **UNSCOPED** (no stream suffix), a Cross-stream impact notice is **NOT** needed (Case B only applies to scoped issues).

## Proposed Remediation Tasks (2.1.x stream)

The affected dependency is in the **Cargo** ecosystem. Per the ecosystem mappings, two remediation tasks are required:

### Task 1: Upstream Backport

```
Summary:    CVE-2026-33501 h2 — backport fix to release/0.3.z
Issue Type: Task (sub-task of TC-8004)
Labels:     CVE-2026-33501, security-backport
Assignee:   Unassigned
Due Date:   2026-08-01 (carried from parent)
Description:
  Backport the h2 fix (>= 0.4.8) to the upstream branch release/0.3.z
  in the rhtpa-backend repository.

  Steps:
  1. Check out the release/0.3.z branch of rhtpa-backend
  2. Update h2 dependency in Cargo.toml to >= 0.4.8
  3. Run `cargo update -p h2` to update Cargo.lock
  4. Verify the h2 version in Cargo.lock is >= 0.4.8
  5. Run tests to confirm no regressions
  6. Submit PR against release/0.3.z

  Upstream fix PR: https://github.com/hyperium/h2/pull/812
  Advisory: https://github.com/advisories/GHSA-2026-kv8p-r3n7

  Parent: TC-8004
```

### Task 2: Downstream Propagation

```
Summary:    CVE-2026-33501 h2 — propagate fix to 2.1.x release repo
Issue Type: Task (sub-task of TC-8004)
Labels:     CVE-2026-33501, security-propagation
Assignee:   Unassigned
Due Date:   2026-08-01 (carried from parent)
Blocks:     TC-8004
Description:
  After the upstream backport (Task 1) merges, propagate the fix into
  the 2.1.x Konflux release repo (rhtpa-release.0.3.z).

  Steps:
  1. Wait for Task 1 (upstream backport to release/0.3.z) to merge
  2. Update artifacts.lock.yaml in rhtpa-release.0.3.z to reference
     the new backend tag that includes the h2 fix
  3. Trigger a new 2.1.x build
  4. Verify the resulting build's Cargo.lock contains h2 >= 0.4.8
  5. Submit PR against rhtpa-release.0.3.z

  Release repo: git.example.com/rhtpa/rhtpa-release.0.3.z

  Parent: TC-8004
  Depends on: Task 1 (upstream backport)
```

## Summary of Proposed Mutations

All mutations are **proposals** — none have been executed.

| # | Action | Target | Details |
|---|--------|--------|---------|
| 1 | Update Affects Versions | TC-8004 | Remove RHTPA 2.2.0, Add RHTPA 2.1.1 |
| 2 | Create Task | Sub-task of TC-8004 | Upstream backport to release/0.3.z |
| 3 | Create Task | Sub-task of TC-8004 | Downstream propagation to 2.1.x release repo |

No remediation tasks are created for the 2.2.x stream because it is not affected.
No Cross-stream impact notice is needed because the issue is unscoped (covers all streams).
