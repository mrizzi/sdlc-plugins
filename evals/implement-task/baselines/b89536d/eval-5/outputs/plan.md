# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.

## Branch Operations

1. **Check out the target branch** (the feature branch specified in the task):
   ```
   git checkout TC-9005
   git pull
   ```

2. **Create the task branch** named after the Jira issue ID:
   ```
   git checkout -b TC-9205
   ```

3. **After implementation, push and create PR targeting the feature branch**:
   ```
   git push -u origin TC-9205
   gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "..."
   ```

The PR must use `--base TC-9005` to target the feature branch, NOT main. This is because the Target Branch field in the task description is `TC-9005`, and the task is incorporated by TC-9005.

## Files to Modify

### 1. `migration/src/lib.rs`
- Register the new migration module `m0002_drop_advisory_status` in the migration list.
- Add a `mod m0002_drop_advisory_status;` declaration at the top of the file (following the existing `mod m0001_initial;` pattern).
- Add `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, after the existing `m0001_initial` entry.

## Files to Create

### 2. `migration/src/m0002_drop_advisory_status/mod.rs`
- Create a new migration module that implements `MigrationTrait` with:
  - `up` method: drops the `status` column from the `advisory` table using `TableAlterStatement`
  - `down` method: re-adds the `status` column as a nullable string for rollback
- Follow the exact pattern from `migration/src/m0001_initial/mod.rs` (implement `MigrationTrait`, use `MigrationName` trait, etc.)

## Pre-implementation Verification

Before implementing:
- Verify that `entity/src/advisory.rs` does NOT reference a `status` column (confirming it has already been removed from the entity definition)
- Inspect `migration/src/m0001_initial/mod.rs` to understand the exact migration pattern (struct name, trait implementations, use statements)
- Inspect `migration/src/lib.rs` to understand how migrations are registered (the `vec![]` pattern in `migrations()`)

## Commit Message

```
feat(migration): add migration to drop advisory status column

Add database migration m0002_drop_advisory_status that drops the
deprecated `status` column from the `advisory` table. The column was
replaced by the `severity` enum field and is no longer referenced by
any service or entity code. The down method re-adds the column as a
nullable string to allow rollback.

Implements TC-9205
```

With the `--trailer="Assisted-by: Claude Code"` flag.

## PR Details

- **Title**: `feat(migration): add migration to drop advisory status column`
- **Base branch**: `TC-9005` (the feature branch, NOT main)
- **Head branch**: `TC-9205` (the task branch)
- **Description**: Will include:
  - Summary of changes (new migration, registration in lib.rs)
  - Link to Jira issue: `Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)`

## Jira Updates

1. Transition TC-9205 to "In Progress" at start
2. Assign to current user
3. After PR creation:
   - Set Git Pull Request custom field (`customfield_10875`) with PR URL in ADF format
   - Add comment with PR link, summary of changes
   - Transition to "In Review"
