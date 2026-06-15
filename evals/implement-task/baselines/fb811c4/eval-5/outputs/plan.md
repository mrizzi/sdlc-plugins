# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.

## Target Branch and Branch Operations

- **Target Branch:** `TC-9005` (feature branch, not main)
- **Task Branch:** `TC-9205` (named after the task issue ID)
- **Branch operations:**
  1. `git checkout TC-9005` -- check out the feature branch
  2. `git pull` -- pull latest changes on the feature branch
  3. `git checkout -b TC-9205` -- create the task branch from the feature branch
- **PR target:** The pull request targets `TC-9005` (the feature branch), NOT `main`
  - Command: `gh pr create --base TC-9005 --head TC-9205 ...`

## Files to Create

### 1. `migration/src/m0002_drop_advisory_status/mod.rs`

New migration file that drops the `status` column from the `advisory` table.

See `outputs/file-1-description.md` for detailed changes.

## Files to Modify

### 2. `migration/src/lib.rs`

Register the new migration module in the migration list.

See `outputs/file-2-description.md` for detailed changes.

## Pre-Implementation Verification

Before implementing, verify:
- The `advisory` entity in `entity/src/advisory.rs` does NOT reference the `status` column (confirming it is safe to drop).
- The existing migration `m0001_initial/mod.rs` to understand the exact pattern for implementing `MigrationTrait`.
- No service code references `Advisory::Status` or the `status` column anywhere.

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the unused
`status` column from the `advisory` table. The column was replaced
by the `severity` enum field and is no longer referenced by any
service or entity code.

The down method re-adds the column as a nullable string to support
rollback.

Implements TC-9205
```

With trailer: `--trailer="Assisted-by: Claude Code"`

## Pull Request

- **Base branch:** `TC-9005`
- **Head branch:** `TC-9205`
- **Title:** `feat(migration): drop deprecated status column from advisory table`
- **Description:**

```markdown
## Summary

Add migration `m0002_drop_advisory_status` that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.

- New migration file: `migration/src/m0002_drop_advisory_status/mod.rs`
- Migration registered in `migration/src/lib.rs`
- Down method re-adds the column as nullable string for rollback

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)

## Test plan

- [ ] Migration runs successfully against a test database (`cargo test`)
- [ ] Rollback (down) re-adds the `status` column as nullable string
- [ ] Existing advisory queries still work after the column is dropped
- [ ] No code references `Advisory::Status` or the `status` column
```

## Jira Updates

1. **Transition:** TC-9205 to "In Progress" at start of implementation
2. **Assign:** TC-9205 to current user
3. **Custom field:** Set `customfield_10875` (Git Pull Request) to the PR URL in ADF format
4. **Comment:** Add comment with PR link, summary of changes, and confirmation of no deviations
5. **Transition:** TC-9205 to "In Review" after PR creation

## Self-Verification Checklist

- [ ] Scope containment: only `migration/src/lib.rs` modified and `migration/src/m0002_drop_advisory_status/mod.rs` created
- [ ] No sensitive patterns in diff
- [ ] Entity `advisory.rs` does not reference `status` column
- [ ] Migration follows same pattern as `m0001_initial`
- [ ] Data-flow trace: migration up drops column, down re-adds it -- complete
- [ ] Contract verification: `MigrationTrait` fully implemented with both `up` and `down`
- [ ] Sibling parity with `m0001_initial`: same trait, same use statements, same async pattern
- [ ] CI checks from CONVENTIONS.md (if applicable): run all extracted commands
