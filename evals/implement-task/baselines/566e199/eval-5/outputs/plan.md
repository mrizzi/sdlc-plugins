# Implementation Plan for TC-9205

## Task Summary

**Jira Issue**: TC-9205
**Summary**: Add migration to drop status table column
**Repository**: trustify-backend
**Target Branch**: TC-9005 (feature branch, extracted from task description's "Target Branch" section)
**Parent Feature**: TC-9005 (linked via "is incorporated by TC-9005")

## Branch Operations

1. **Check out the Target Branch (TC-9005)**:
   ```
   git checkout TC-9005
   git pull
   ```
   The Target Branch is TC-9005, a feature branch -- NOT main. This is extracted from the
   "Target Branch" section of the task description.

2. **Create the task branch (TC-9205)**:
   ```
   git checkout -b TC-9205
   ```
   The task branch is named after the Jira issue ID (TC-9205), NOT the feature branch (TC-9005).

3. **After implementation, push and create PR targeting TC-9005**:
   ```
   git push -u origin TC-9205
   gh pr create --base TC-9005 --head TC-9205 \
     --title "feat(migration): add migration to drop advisory status column" \
     --body "## Summary

   Add a database migration that drops the deprecated \`status\` column from the
   \`advisory\` table. The column was replaced by the \`severity\` enum field in a
   previous migration and is no longer referenced by any service or entity code.

   Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)"
   ```
   The PR targets `--base TC-9005` (the feature branch), NOT `--base main`.

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the unused status
column from the advisory table. The column was replaced by the severity
enum field and is no longer referenced by service or entity code. The
down method re-adds the column as a nullable string for rollback support.

Implements TC-9205
```

With the trailer flag: `--trailer="Assisted-by: Claude Code"`

Full command:
```
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the unused status
column from the advisory table. The column was replaced by the severity
enum field and is no longer referenced by service or entity code. The
down method re-adds the column as a nullable string for rollback support.

Implements TC-9205"
```

## Files to Modify

1. **`migration/src/lib.rs`** -- Register the new migration module in the migration list

## Files to Create

1. **`migration/src/m0002_drop_advisory_status/mod.rs`** -- Migration that drops the `status` column from the `advisory` table

## Pre-Implementation Verification (Step 4)

Before implementing, the following inspections would be performed:

1. **Inspect `migration/src/m0001_initial/mod.rs`** -- Understand the existing migration pattern: struct definition, `MigrationTrait` implementation, `up`/`down` methods, use of `TableAlterStatement` vs `TableCreateStatement`
2. **Inspect `migration/src/lib.rs`** -- Understand how migrations are registered in the `migrations()` function and the `vec![]` pattern
3. **Inspect `entity/src/advisory.rs`** -- Verify that the `status` column is NOT referenced in the entity definition (confirms it is safe to drop)
4. **Search for `status` references** -- Grep across the codebase for any remaining references to `Advisory::Status` or the `status` column on the advisory table to ensure nothing still reads/writes it
5. **Check CONVENTIONS.md** -- Read the repository's CONVENTIONS.md for coding standards, CI check commands, and naming rules

## Implementation Steps

### Step 1: Create `migration/src/m0002_drop_advisory_status/mod.rs`

- Define a struct (e.g., `Migration`) implementing `MigrationTrait`
- Implement `name()` returning a descriptive migration name
- Implement `up()` using `manager.alter_table()` with `Table::alter().table(Advisory::Table).drop_column(Advisory::Status)` to drop the column
- Implement `down()` using `manager.alter_table()` with `Table::alter().table(Advisory::Table).add_column(ColumnDef::new(Advisory::Status).string().null())` to re-add as nullable string
- Follow the exact pattern from `m0001_initial/mod.rs`

### Step 2: Modify `migration/src/lib.rs`

- Add `mod m0002_drop_advisory_status;` declaration
- Add `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, following the pattern of `m0001_initial`

### Step 3: Verify acceptance criteria

- Confirm the migration drops the `status` column
- Confirm the `down` method re-adds it as nullable string
- Confirm the migration is registered in `lib.rs`
- Grep for any remaining `status` column references in service/entity code

### Step 4: Run tests

- Run `cargo test` to verify migration compiles and tests pass
- Verify existing advisory queries still work

## Jira Updates (Step 11)

1. Update `customfield_10875` (Git Pull Request) with the PR URL in ADF format
2. Add a comment summarizing the changes and linking to the PR
3. Transition TC-9205 to "In Review"
