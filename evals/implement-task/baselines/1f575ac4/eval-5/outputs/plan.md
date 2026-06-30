# Implementation Plan: TC-9205 — Add migration to drop status table column

## Target Branch Extraction

The task description specifies **Target Branch: TC-9005**. This is a feature branch (linked issue: "is incorporated by TC-9005"), not `main`. All branch operations and PR targeting must use TC-9005 as the base.

## Branch Operations

1. **Checkout the target branch and pull latest**:
   ```
   git checkout TC-9005 && git pull
   ```
   This checks out the feature branch TC-9005 (NOT main) as specified in the Target Branch section of the task.

2. **Create the task branch from the target branch**:
   ```
   git checkout -b TC-9205
   ```
   The task branch is named TC-9205 (the Jira issue ID for this task), NOT TC-9005 (the feature branch).

3. **Open PR targeting the feature branch**:
   ```
   gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "..."
   ```
   The PR is opened with `--base TC-9005` to target the feature branch, NOT `--base main`.

## Pre-Implementation: Inspect Existing Code (Constraint 1.5)

Before making any changes, read and analyze the following existing files to understand patterns and verify assumptions:

1. **`migration/src/m0001_initial/mod.rs`** — Inspect the existing migration to understand the migration pattern: how `MigrationTrait` is implemented, what imports are used, the structure of `up` and `down` methods, and how SeaORM migration types are referenced. This is the sibling migration that establishes the convention for all new migrations.

2. **`entity/src/advisory.rs`** — Verify that the `advisory` entity no longer references the `status` column. The task description states this column was replaced by a `severity` enum field, and we must confirm no code still depends on `status` before dropping it.

3. **`migration/src/lib.rs`** — Inspect how existing migrations are registered in the `migrations()` function to understand the pattern for adding new entries to the migration vector.

## Files to Create

### 1. `migration/src/m0002_drop_advisory_status/mod.rs`

New migration module that drops the deprecated `status` column from the `advisory` table. Follows the pattern established by `m0001_initial/mod.rs`:

- Implements `MigrationTrait` for a `Migration` struct
- `up` method: Uses `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await` to drop the column
- `down` method: Re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` to allow rollback
- `name()` method: Returns a migration name string following the naming convention from m0001

## Files to Modify

### 2. `migration/src/lib.rs`

Register the new migration module by:
- Adding `mod m0002_drop_advisory_status;` declaration
- Adding `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, after the existing `m0001_initial` entry

## Commit Message

Following Conventional Commits format with Jira ID in footer and assisted-by trailer:

```
feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that removes the deprecated
status column from the advisory table. The column was replaced by the
severity enum field and is no longer referenced by any service or
entity code.

TC-9205
```

Committed with:
```
git commit --trailer='Assisted-by: Claude Code'
```

## Verification

- Confirm `entity/src/advisory.rs` has no references to a `status` column
- Confirm the migration follows the same pattern as `m0001_initial/mod.rs`
- Confirm the migration is properly registered in `migration/src/lib.rs`
- Confirm no other service code references the `status` column on the advisory table
