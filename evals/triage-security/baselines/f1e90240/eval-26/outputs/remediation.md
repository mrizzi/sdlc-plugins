# Step 8 -- Remediation

## Triage Outcome: Case A -- Affected (with dev-dependency modifications)

All 2.2.x versions ship criterion 0.5.1 (affected). However, criterion is a
**dev-only dependency** (declared in `[dev-dependencies]`), so remediation tasks
carry the `dev-dependency` label and Normal priority override.

Cross-stream impact (Case B): The 2.1.x stream is also affected but is outside
this issue's scope. A cross-stream impact comment would be posted to TC-8050.

---

## Remediation Task 1: Upstream Backport (source repo fix)

**Summary**: Remediate CVE-2026-99001: bump criterion to 0.5.2 (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal

### Task Description

## Repository

rhtpa-backend

## Target Branch

release/0.4.z

## Description

Remediate CVE-2026-99001: path traversal in benchmark output in criterion.
The vulnerable dependency (criterion < 0.5.2) must be updated to the fixed
version (0.5.2+).

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

Affected versions: RHTPA 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4
Source commits: v0.4.5, v0.4.8, v0.4.11, v0.4.12

CVE record: https://www.cve.org/CVERecord?id=CVE-2026-99001

## Implementation Notes

- Target branch: release/0.4.z
- **Dependency type**: direct dev-dependency
- **Dependency scope**: dev-only ([dev-dependencies] in backend/Cargo.toml) -- NOT shipped in production builds, used for benchmarks only
- Priority overridden to Normal due to dev-only scope

### Remediation approach (direct dependency)

- Update criterion dependency to >= 0.5.2 in backend/Cargo.toml `[dev-dependencies]`
- Run `cargo update -p criterion` to update Cargo.lock
- If a direct bump introduces breaking changes, assess whether a code-level
  workaround is viable (see upstream changelog)

## Acceptance Criteria

- [ ] criterion dependency is >= 0.5.2
- [ ] No other dependency conflicts introduced
- [ ] Existing tests pass

## Test Requirements

- [ ] Existing test suite passes with the updated dependency

## Dependencies

- Depends on: TC-8050 (parent tracking issue)

---

## Remediation Task 2: Downstream Propagation (Konflux release repo update)

**Summary**: Propagate CVE-2026-99001 fix: update rhtpa-backend ref in rhtpa-release.0.4.z (rhtpa-2.2)

**Labels**: `ai-generated-jira`, `Security`, `CVE-2026-99001`, `dev-dependency`

**Priority**: Normal

### Task Description

## Repository

rhtpa-release.0.4.z

## Target Branch

main

## Description

Update rhtpa-backend reference in rhtpa-release.0.4.z to pick up the
CVE-2026-99001 fix from the upstream backport task.

The upstream backport bumps criterion to 0.5.2 on release/0.4.z. Once
that PR merges, update the source pinning in this Konflux release repo
so the next build ships the fix.

This dependency is dev/build-only and is not shipped in production.
Remediation priority is Normal (supply chain risk only).

## Implementation Notes

- Source pinning method: artifacts.lock.yaml (download URL contains tag)
- **Dependency type**: direct dev-dependency -- carried forward from upstream task
- **Dependency scope**: dev-only -- NOT shipped in production
- Update the rhtpa-backend reference to the merged commit or new release tag
- Verify the Konflux build pipeline triggers successfully

## Acceptance Criteria

- [ ] rhtpa-backend reference updated to include the fix
- [ ] Konflux rebuild triggers new container image

## Test Requirements

- [ ] Container image builds successfully with the updated reference

## Dependencies

- Depends on: upstream backport task (upstream backport must merge first)
- Depends on: TC-8050 (parent tracking issue)

---

## Jira Operations Summary

### Task Creation

1. Create upstream backport task with labels `["ai-generated-jira", "Security", "CVE-2026-99001", "dev-dependency"]` and **Normal** priority
2. Post description digest comment on upstream task (re-fetch description, compute SHA-256 via `scripts/sha256-digest.py`, post `[sdlc-workflow] Description digest: <tagged-digest>`)
3. Create downstream propagation task with labels `["ai-generated-jira", "Security", "CVE-2026-99001", "dev-dependency"]` and **Normal** priority
4. Post description digest comment on downstream task (re-fetch description, compute SHA-256 via `scripts/sha256-digest.py`, post `[sdlc-workflow] Description digest: <tagged-digest>`)

### Linkage

1. Link upstream task to TC-8050 with "Depend" link type
2. Link downstream task to TC-8050 with "Depend" link type
3. Link downstream task as blocked by upstream task with "Blocks" link type
4. Transition TC-8050 to In Progress

### Cross-Stream Impact Comment (Case B)

Post comment to TC-8050:
```
Cross-stream impact: criterion < 0.5.2 also affects stream 2.1.x based on
lock file analysis. This stream is tracked by companion issues (see Related
links) or may require separate PSIRT triage.
```

### Dev-Dependency Priority Override Rationale

criterion is declared in `[dev-dependencies]` in backend/Cargo.toml and is NOT
present in production builds. Per the dependency scope decision tree in
version-impact-analysis.md:

- Dev-only dependencies still represent a supply chain risk
- Remediation tasks are created but with the `dev-dependency` label
- Priority is set to **Normal** regardless of CVE severity (CVSS 5.3 Medium)
- Task descriptions include a note about the dev/build-only scope

### Post-Triage Summary

Add `ai-cve-triaged` label to TC-8050 and post summary comment documenting:
1. Version impact table (all 2.2.x versions affected, criterion 0.5.1 < 0.5.2)
2. Dependency scope: dev-only, not shipped in production
3. Remediation tasks created with dev-dependency label and Normal priority
4. Cross-stream impact on 2.1.x noted
