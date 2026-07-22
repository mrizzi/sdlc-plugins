# Implementation Plan for TC-9205

## Task Summary

**Jira ID**: TC-9205
**Summary**: Add migration to drop status table column
**Repository**: trustify-backend
**Target Branch**: TC-9005 (feature branch)
**Parent Feature**: TC-9005 (linked via "is incorporated by")
**Dependencies**: None

## Branch Operations

1. **Checkout the target (feature) branch**:
   ```
   git checkout TC-9005
   git pull
   ```
2. **Create the task branch from the feature branch**:
   ```
   git checkout -b TC-9205
   ```
   The task branch is named after the task ID (TC-9205), NOT after the target branch.

3. **After implementation, push and create PR targeting the feature branch**:
   ```
   git push -u origin TC-9205
   gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "..."
   ```
   The PR targets `TC-9005` (the feature branch), NOT `main`.

   Fork detection would be performed first:
   ```
   git remote get-url upstream 2>/dev/null
   ```
   If a fork is detected, the PR create command would include `-R <upstream-owner/repo> --head <fork-owner>:TC-9205`.

## Files to Modify

1. **`migration/src/lib.rs`** -- Register the new migration module in the migration list

## Files to Create

1. **`migration/src/m0002_drop_advisory_status/mod.rs`** -- Migration that drops the `status` column from the `advisory` table

## Pre-Implementation Verification (Step 4)

Before implementing, the following inspections would be performed:

1. **Inspect `migration/src/lib.rs`** using Serena (`mcp__serena_backend__get_symbols_overview`) to understand the current migration registration pattern and see how `m0001_initial` is registered.

2. **Inspect `migration/src/m0001_initial/mod.rs`** using Serena (`mcp__serena_backend__find_symbol`) to understand the existing migration pattern -- specifically how `MigrationTrait` is implemented with `up` and `down` methods.

3. **Inspect `entity/src/advisory.rs`** using Serena to verify that the `Advisory` entity no longer references the `status` column, confirming it is safe to drop.

4. **Search for references to `status` column** using `mcp__serena_backend__search_for_pattern` or Grep across the codebase (especially in `modules/fundamental/src/advisory/`, `modules/ingestor/src/graph/advisory/`, and `tests/api/advisory.rs`) to confirm no service or entity code references the `status` column.

5. **Check `CONVENTIONS.md`** at the repository root for project-level conventions and CI check commands.

6. **Convention conformance analysis** -- examine `m0001_initial/mod.rs` as the sibling migration to discover patterns for naming, structure, imports, and error handling.

7. **Documentation file identification** -- check for README files in `migration/` and related API docs.

## Implementation Details (Step 6)

### File 1: `migration/src/m0002_drop_advisory_status/mod.rs` (CREATE)

Create a new migration module following the pattern established by `m0001_initial/mod.rs`:
- Implement `MigrationTrait` with `up` and `down` methods
- `up`: Use `TableAlterStatement` to drop the `status` column from the `advisory` table
- `down`: Re-add the column as `ColumnDef::new(Advisory::Status).string().null()` for rollback
- Include proper documentation comments on the struct and methods

### File 2: `migration/src/lib.rs` (MODIFY)

Register the new migration module:
- Add `mod m0002_drop_advisory_status;` declaration
- Add the migration to the `vec![]` in the `migrations()` function, following the pattern used for `m0001_initial`

## Tests (Step 7)

Per Test Requirements:
- Test that the migration runs successfully against a test database
- Test that the rollback (down) re-adds the column
- Verify that existing advisory queries still work after the column is dropped

These would be added as integration tests, potentially in `tests/api/advisory.rs` or a dedicated migration test file, following the project's existing test patterns (using `assert_eq!(resp.status(), StatusCode::OK)` pattern, real PostgreSQL test database).

## Acceptance Criteria Verification (Step 8)

1. Migration drops the `status` column from the `advisory` table -- verified by inspecting the `up` method
2. Migration `down` method re-adds the column as nullable string for rollback -- verified by inspecting the `down` method
3. Migration is registered in `migration/src/lib.rs` -- verified by checking the `migrations()` function
4. No service or entity code references the `status` column -- verified by codebase search in Step 4

## Commit Message

```
feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that removes the deprecated
`status` column from the `advisory` table. The column was replaced by
the `severity` enum field in a previous migration and is no longer
referenced by any service or entity code.

The down method re-adds the column as a nullable string to support
rollback.

Implements TC-9205
```

With the trailer: `--trailer="Assisted-by: Claude Code"`

## PR Details

- **Title**: `feat(migration): add migration to drop advisory status column`
- **Base branch**: `TC-9005` (the feature branch, NOT main)
- **Head branch**: `TC-9205`
- **Description body** would include:
  - Summary of changes
  - `Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)`

## Jira Updates (Step 11)

1. Update Git Pull Request custom field (`customfield_10875`) with the PR URL (in ADF format)
2. Add comment to TC-9205 with PR link and summary of changes
3. Transition TC-9205 to "In Review"
