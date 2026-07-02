# Implementation Plan for TC-9205: Add migration to drop status table column

## Step 0 -- Validate Project Configuration

CLAUDE.md contains all required sections:
- Repository Registry: trustify-backend mapped to `./` with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence: serena_backend instance with rust-analyzer

Validation passes.

## Step 1 -- Fetch and Parse Jira Task

Parsed fields from task description:

- **Key**: TC-9205
- **Summary**: Add migration to drop status table column
- **Repository**: trustify-backend
- **Target Branch**: TC-9005
- **Description**: Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.
- **Files to Modify**: `migration/src/lib.rs` -- register the new migration module in the migration list
- **Files to Create**: `migration/src/m0002_drop_advisory_status/mod.rs` -- migration that drops the `status` column from the `advisory` table
- **Implementation Notes**: Follow the existing migration pattern in `m0001_initial/mod.rs`, implement `MigrationTrait` with `up` (drop column) and `down` (re-add column) methods, use SeaORM's `TableAlterStatement`, register in `lib.rs` `migrations()` function
- **Target PR**: not present
- **Bookend Type**: not present
- **Dependencies**: None

All required sections are present. No gaps found.

### Target Branch extraction

Target Branch is **TC-9005** (a feature branch). This will be used as:
1. The branch to checkout before creating the task branch (Step 5)
2. The `--base` argument for `gh pr create` (Step 10)

## Step 2 -- Verify Dependencies

No dependencies listed. Skip.

## Step 3 -- Transition to In Progress and Assign

1. Call `jira.user_info()` to get current user's account ID
2. Call `jira.edit_issue(TC-9205, assignee=<account-id>)` to assign
3. Call `jira.transition_issue(TC-9205)` to transition to In Progress

## Step 4 -- Understand the Code

### Files to inspect

1. **`migration/src/lib.rs`** -- Use `mcp__serena_backend__get_symbols_overview` to understand its structure. Specifically look for the `migrations()` function and how `m0001_initial` is registered in the `vec![]`. This tells us the exact pattern for adding a new migration module.

2. **`migration/src/m0001_initial/mod.rs`** -- This is the sibling migration file. Use `mcp__serena_backend__get_symbols_overview` to see its structure, then `mcp__serena_backend__find_symbol` with `include_body=true` on the `MigrationTrait` implementation to understand the exact pattern for `up()` and `down()` methods. This is the template for the new migration.

3. **`entity/src/advisory.rs`** -- Verify that the `status` column is no longer referenced in the advisory entity. Use `mcp__serena_backend__get_symbols_overview` to see what columns are defined. Confirm `Status` variant is absent from the entity's column enum.

4. **Search for `status` references** -- Use `mcp__serena_backend__search_for_pattern` (or Grep as fallback) to search for any remaining references to `Advisory::Status` or `advisory.status` across the codebase. Confirm no service or entity code references the column.

5. **`CONVENTIONS.md`** -- Check for repository root CONVENTIONS.md using `mcp__serena_backend__list_dir` or Glob. Read it if present and extract CI check commands and conventions.

### Convention conformance analysis (sibling analysis)

Sibling file for the new migration: `migration/src/m0001_initial/mod.rs`

Patterns to examine:
- Module declaration style in `lib.rs`
- `MigrationTrait` implementation pattern (struct definition, `MigrationName`, `up`, `down`)
- Use of SeaORM types (`Table`, `ColumnDef`, `Manager`)
- Import conventions
- Error handling (`Result` return type from migration methods)

### Test convention analysis

Test files to examine: `tests/api/advisory.rs` (sibling advisory test)

Patterns to examine:
- Test assertion style (`assert_eq!` with `StatusCode`)
- Database test setup patterns
- Test naming conventions

### Documentation file identification

- `README.md` at repository root
- `CONVENTIONS.md` at repository root (if it exists)
- No API documentation is impacted (this is a migration, not an endpoint change)

## Step 5 -- Create Branch

**This is a default flow (no Target PR, no Bookend Type).**

The Target Branch is **TC-9005** (a feature branch). Branch operations:

```bash
git checkout TC-9005
git pull
git checkout -b TC-9205
```

This creates the task branch `TC-9205` from the feature branch `TC-9005`.

## Step 6 -- Implement Changes

### File 1: Create `migration/src/m0002_drop_advisory_status/mod.rs`

Create a new migration module following the pattern from `m0001_initial/mod.rs`:
- Define a struct (e.g., `Migration`)
- Implement `MigrationTrait` with:
  - `name()` returning the migration name
  - `up()` using `TableAlterStatement` to drop the `status` column from `advisory`
  - `down()` using `TableAlterStatement` to re-add the `status` column as a nullable string
- Use SeaORM types: `sea_orm_migration::prelude::*`
- Use `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await` for the up migration
- Use `ColumnDef::new(Advisory::Status).string().null()` in the down migration

### File 2: Modify `migration/src/lib.rs`

- Add `mod m0002_drop_advisory_status;` module declaration (following the pattern of `mod m0001_initial;`)
- Add `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, after the `m0001_initial` entry

### Verification before implementation

Before writing code, verify:
1. `entity/src/advisory.rs` does NOT reference `status` column (confirming it is safe to drop)
2. No service code in `modules/fundamental/src/advisory/` references `status`
3. No ingestor code in `modules/ingestor/src/graph/advisory/` references `status`

## Step 7 -- Write Tests

Tests would verify:
1. Migration runs successfully (up method drops the `status` column)
2. Rollback works (down method re-adds the column as nullable string)
3. Existing advisory queries still work after the column is dropped

Following test conventions from `tests/api/advisory.rs`:
- Use `assert_eq!` pattern
- Use test database setup patterns from sibling tests
- Name tests as `test_<action>_<scenario>` (e.g., `test_migration_drop_status_column`)
- Add doc comments to every test function

## Step 8 -- Verify Acceptance Criteria

1. Migration drops the `status` column from the `advisory` table -- verified by `up()` implementation
2. Migration `down` method re-adds the column as nullable string for rollback -- verified by `down()` implementation
3. Migration is registered in `migration/src/lib.rs` -- verified by module declaration and vec entry
4. No service or entity code references the `status` column -- verified by codebase search in Step 4

## Step 9 -- Self-Verification

### Scope containment
- `git diff --name-only` should show only:
  - `migration/src/lib.rs` (modified)
  - `migration/src/m0002_drop_advisory_status/mod.rs` (created)
- Both are within scope per Files to Modify and Files to Create

### Sensitive-pattern check
- No passwords, API keys, or secrets expected in migration code
- Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` to confirm

### Data-flow trace
- Migration `up()`: receives manager -> alters table -> drops column -> returns Result -- COMPLETE
- Migration `down()`: receives manager -> alters table -> adds column -> returns Result -- COMPLETE

### Contract & sibling parity
- `MigrationTrait` contract: `name()`, `up()`, `down()` all implemented
- Sibling parity with `m0001_initial`: same struct pattern, same trait implementation, same error handling

## Step 10 -- Commit and Push

### Commit message

```
feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that drops the deprecated status
column from the advisory table. The column was replaced by the severity
enum field and is no longer referenced by any service or entity code.

Implements TC-9205
```

### Commit command

```bash
git add migration/src/m0002_drop_advisory_status/mod.rs migration/src/lib.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that drops the deprecated status
column from the advisory table. The column was replaced by the severity
enum field and is no longer referenced by any service or entity code.

Implements TC-9205"
```

### Push and create PR

```bash
git push -u origin TC-9205
gh pr create --base TC-9005 --head TC-9205 \
  --title "feat(migration): add migration to drop advisory status column" \
  --body "## Summary

- Add m0002_drop_advisory_status migration that drops the deprecated \`status\` column from the \`advisory\` table
- Register the new migration in \`migration/src/lib.rs\`
- The \`down\` method re-adds the column as a nullable string for rollback

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)"
```

Key PR details:
- **`--base TC-9005`**: PR targets the feature branch TC-9005, NOT main
- **`--head TC-9205`**: PR is from the task branch TC-9205

## Step 11 -- Update Jira

1. Update Git Pull Request custom field (`customfield_10875`) on TC-9205 with the PR URL in ADF format
2. Add a comment to TC-9205 summarizing:
   - PR link
   - Changes: created migration m0002_drop_advisory_status to drop the deprecated status column; registered migration in lib.rs
   - No deviations from the plan
3. Transition TC-9205 to In Review
