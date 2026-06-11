# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.

## Jira Issue

- **Key**: TC-9205
- **Summary**: Add migration to drop status table column
- **Status**: To Do
- **Labels**: ai-generated-jira
- **Parent Feature**: TC-9005 (linked via "is incorporated by")

## Target Branch and Branch Operations

### Target Branch

The **Target Branch** specified in the task is `TC-9005`. This is a feature branch (not `main`), indicating this task is part of a feature-branch workflow where multiple tasks are implemented on a shared feature branch before being merged to main.

### Branch Operations

1. **Checkout the target branch**:
   ```
   git checkout TC-9005
   git pull
   ```

2. **Create the task branch from the target branch**:
   ```
   git checkout -b TC-9205
   ```
   This creates a new branch `TC-9205` based on the `TC-9005` feature branch.

3. **After implementation, push and create PR**:
   ```
   git push -u origin TC-9205
   gh pr create --base TC-9005 --head TC-9205 --title "feat(migration): add migration to drop advisory status column" --body "..."
   ```
   The PR targets the `TC-9005` feature branch (not `main`), since that is the Target Branch specified in the task.

### Commit Message

```
feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the unused status
column from the advisory table. The column was replaced by the severity
enum field in a previous migration and is no longer referenced by any
service or entity code.

The down method re-adds the column as a nullable string to allow rollback.

Implements TC-9205
```

The commit would include the trailer: `--trailer="Assisted-by: Claude Code"`

### PR Description

The PR description would include:

```
## Summary

- Add new migration `m0002_drop_advisory_status` that drops the deprecated `status` column from the `advisory` table
- Register the migration in `migration/src/lib.rs`
- The `down` method re-adds the column as a nullable string for safe rollback

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)
```

The PR would target `TC-9005` as the base branch via `--base TC-9005`.

## Files to Create

1. **`migration/src/m0002_drop_advisory_status/mod.rs`** — New migration module that drops the `status` column from the `advisory` table
   - See `outputs/file-1-description.md` for detailed changes

## Files to Modify

1. **`migration/src/lib.rs`** — Register the new migration module in the migration list
   - See `outputs/file-2-description.md` for detailed changes

## Pre-Implementation Verification

Before implementing, the following would be verified:

1. **Entity verification**: Confirm that `entity/src/advisory.rs` does NOT reference a `status` column — the task states it was already removed from the entity
2. **Service code verification**: Grep the codebase for any references to the `status` column on the `advisory` table to confirm no code reads or writes it
3. **Sibling migration analysis**: Read `migration/src/m0001_initial/mod.rs` to understand the exact migration pattern (imports, trait implementation, method signatures)
4. **CONVENTIONS.md**: Read `trustify-backend/CONVENTIONS.md` for any CI check commands or code conventions
5. **Migration lib.rs structure**: Read `migration/src/lib.rs` to understand how migrations are registered (module declarations and the `migrations()` function)

## Post-Implementation Verification

1. **Scope containment**: `git diff --name-only` should show only:
   - `migration/src/m0002_drop_advisory_status/mod.rs` (new)
   - `migration/src/lib.rs` (modified)

2. **Untracked file check**: Verify `migration/src/m0002_drop_advisory_status/mod.rs` is staged

3. **Sensitive pattern check**: Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` to ensure no secrets

4. **CI checks**: Run any CI check commands from CONVENTIONS.md, plus `cargo test` and `cargo build`

5. **Acceptance criteria verification**:
   - Migration drops the `status` column from the `advisory` table
   - Migration `down` method re-adds the column as nullable string for rollback
   - Migration is registered in `migration/src/lib.rs`
   - No service or entity code references the `status` column

6. **Data-flow trace**:
   - Migration `up()`: alter table -> drop column -> complete
   - Migration `down()`: alter table -> add column (nullable string) -> complete
   - Both paths are self-contained with no external dependencies

7. **Contract verification**: The migration implements `MigrationTrait` which requires `up()` and `down()` async methods — both are implemented

## Jira Updates

After PR creation:

1. **Set Git Pull Request custom field** (`customfield_10875`) to the PR URL using ADF format
2. **Add Jira comment** with:
   - PR link
   - Summary of changes (migration created, registered, entity verified)
   - Note that no deviations from the plan were needed
   - Comment footer with sdlc-workflow version link
3. **Transition** TC-9205 to **In Review**
