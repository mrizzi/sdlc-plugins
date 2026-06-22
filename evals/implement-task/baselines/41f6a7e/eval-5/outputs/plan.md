# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

**Jira Issue**: TC-9205
**Summary**: Add a database migration that drops the deprecated `status` column from the `advisory` table.
**Repository**: trustify-backend
**Target Branch**: TC-9005 (feature branch, NOT main)
**Linked Feature**: TC-9005 (this task is incorporated by the feature branch)

## Target Branch

The Target Branch specified in the task description is **TC-9005**. This is a feature branch, not main. All branch operations and the PR must target this branch.

## Branch Operations

1. **Check out the target branch (TC-9005)** and pull latest changes:
   ```
   git checkout TC-9005
   git pull
   ```
2. **Create the task branch** named after the Jira issue ID (TC-9205, NOT TC-9005):
   ```
   git checkout -b TC-9205
   ```

The task branch is named `TC-9205` (the task issue ID). The base branch is `TC-9005` (the feature branch).

## Pre-Implementation Inspection (Step 4 -- Understand the Code)

Before making any changes, inspect the existing codebase using the Serena instance `serena_backend` (from the Repository Registry in CLAUDE.md):

1. **Inspect `migration/src/lib.rs`** using `mcp__serena_backend__get_symbols_overview` to understand how migrations are registered. Look for the `migrations()` function and the `vec![]` that lists migration modules.

2. **Inspect `migration/src/m0001_initial/mod.rs`** using `mcp__serena_backend__get_symbols_overview` and `mcp__serena_backend__find_symbol` with `include_body=true` to understand the existing migration pattern -- specifically the `MigrationTrait` implementation with `up` and `down` methods.

3. **Inspect `entity/src/advisory.rs`** using `mcp__serena_backend__get_symbols_overview` to verify that the `Advisory` entity no longer references the `status` column. This is an explicit prerequisite from the Implementation Notes.

4. **Search for any remaining references to `Advisory::Status`** using `mcp__serena_backend__search_for_pattern` across the codebase to confirm no service or entity code references the `status` column.

5. **Check for `CONVENTIONS.md`** at the repository root (`./CONVENTIONS.md`) -- the repo structure shows it exists. Read it to discover project-level conventions and any CI check commands.

6. **Convention conformance analysis**: Examine `m0001_initial/mod.rs` as the sibling migration file to identify patterns for naming, structure, error handling, and module organization.

7. **Test convention analysis**: Inspect test files in `tests/api/advisory.rs` (sibling advisory tests) to understand test patterns, assertion styles, and naming conventions.

8. **Documentation file identification**: Note `README.md` at the repository root and `docs/architecture.md`, `docs/api.md` as documentation files that may need review (though unlikely for a migration-only change).

## Files to Modify

### 1. `migration/src/lib.rs`
- Register the new migration module `m0002_drop_advisory_status` in the migration list
- Add `mod m0002_drop_advisory_status;` module declaration
- Add `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, following the pattern of `m0001_initial`

## Files to Create

### 2. `migration/src/m0002_drop_advisory_status/mod.rs`
- Create a new migration module that implements `MigrationTrait`
- `up` method: drops the `status` column from the `advisory` table using `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await`
- `down` method: re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` to allow rollback
- Follow the exact pattern from `m0001_initial/mod.rs` for imports, struct definition, and trait implementation

## Commit Message

```
feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the unused `status`
column from the `advisory` table. The column was replaced by the `severity`
enum field in a previous migration and is no longer referenced by any
service or entity code.

The down method re-adds the column as a nullable string for rollback safety.

Implements TC-9205
```

With the trailer flag: `--trailer='Assisted-by: Claude Code'`

Full commit command:
```
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the unused status
column from the advisory table. The column was replaced by the severity
enum field in a previous migration and is no longer referenced by any
service or entity code.

The down method re-adds the column as a nullable string for rollback safety.

Implements TC-9205"
```

## Push and PR

Push the task branch and create a PR targeting the feature branch TC-9005 (NOT main):

```
git push -u origin TC-9205
gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "..."
```

The PR description will include:
- Summary of changes
- Link to Jira issue: `Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)`
- The `--base TC-9005` flag ensures the PR targets the feature branch

## Jira Updates (Step 11)

1. Update the Git Pull Request custom field (`customfield_10875`) with the PR URL in ADF format
2. Add a comment summarizing the changes and linking the PR
3. Transition TC-9205 to **In Review**

## Verification Steps (Step 8-9)

1. Verify acceptance criteria:
   - Migration drops the `status` column from the `advisory` table
   - Migration `down` method re-adds the column as nullable string for rollback
   - Migration is registered in `migration/src/lib.rs`
   - No service or entity code references the `status` column (verified in Step 4)

2. Self-verification:
   - Run `git diff --name-only` to verify only in-scope files are modified
   - Run `git status --short` to check for untracked files
   - Run sensitive-pattern check on staged diff
   - Run CI checks from CONVENTIONS.md (if extracted)
   - Run `cargo test` to verify tests pass
   - Data-flow trace: migration up drops column, migration down re-adds column -- complete lifecycle
   - Contract verification: `MigrationTrait` requires `up` and `down` methods -- both implemented
   - Sibling parity with `m0001_initial`: ensure same patterns for imports, struct, trait impl
