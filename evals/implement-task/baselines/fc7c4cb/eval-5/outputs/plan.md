# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

Add a database migration that drops the deprecated `status` column from the `advisory`
table. The column was replaced by the `severity` enum field in a previous migration and
is no longer read or written by any service code.

## Project Configuration Validation (Step 0)

The project CLAUDE.md contains all required sections:
- **Repository Registry**: `trustify-backend` with Serena instance `serena_backend` at path `./`
- **Jira Configuration**: Project key `TC`, Cloud ID, Feature issue type ID `10142`, Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`
- **Code Intelligence**: Serena instance `serena_backend` with `rust-analyzer`

Configuration is valid; proceeding.

## Task Parsing (Step 1)

- **Jira Issue**: TC-9205
- **Repository**: trustify-backend
- **Target Branch**: TC-9005 (a feature branch, NOT main)
- **Linked Issues**: is incorporated by TC-9005
- **Bookend Type**: none (standard implementation task)
- **Target PR**: none (new branch and PR)

### Files to Modify
- `migration/src/lib.rs` -- register the new migration module in the migration list

### Files to Create
- `migration/src/m0002_drop_advisory_status/mod.rs` -- migration that drops the `status` column

### Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs`
- Implement `MigrationTrait` with `up` (drop column) and `down` (re-add column) methods
- Verify `entity/src/advisory.rs` no longer references the `status` column
- Use SeaORM's `TableAlterStatement` to drop the column
- Register the new migration in `migration/src/lib.rs` by adding it to the `vec![]` in `migrations()`
- The `down` method should re-add the column as `ColumnDef::new(Advisory::Status).string().null()`

### Acceptance Criteria
- Migration drops the `status` column from the `advisory` table
- Migration `down` method re-adds the column as nullable string for rollback
- Migration is registered in `migration/src/lib.rs`
- No service or entity code references the `status` column

### Test Requirements
- Test that the migration runs successfully against a test database
- Test that the rollback (down) re-adds the column
- Verify that existing advisory queries still work after the column is dropped

## Branch Operations (Step 5)

Since the **Target Branch is TC-9005** (a feature branch), NOT main, the branch
operations are:

```bash
git checkout TC-9005
git pull
git checkout -b TC-9205
```

This creates the task branch `TC-9205` based on the feature branch `TC-9005`.
The task branch is named after the task issue ID (TC-9205), which is distinct from
the parent feature branch (TC-9005).

## Code Inspection Plan (Step 4)

Before implementing, inspect the following files using the `serena_backend` Serena
instance (tools called as `mcp__serena_backend__<tool>`):

1. **`migration/src/m0001_initial/mod.rs`** -- use `mcp__serena_backend__get_symbols_overview`
   to understand the existing migration pattern (struct, `MigrationTrait` implementation,
   `up`/`down` methods, column definitions, table alter statements)

2. **`entity/src/advisory.rs`** -- use `mcp__serena_backend__get_symbols_overview` to
   verify that the `status` column is no longer referenced in the entity definition.
   Additionally use `mcp__serena_backend__search_for_pattern` to search for any
   remaining references to `Status` or `status` in the advisory entity.

3. **`migration/src/lib.rs`** -- use `mcp__serena_backend__get_symbols_overview` to
   see the current migration registration pattern (the `migrations()` function and its
   `vec![]` list).

4. **Sibling analysis**: `m0001_initial/mod.rs` is the primary sibling for the new
   migration file. Inspect its structure to capture conventions.

5. **CONVENTIONS.md**: check for `./CONVENTIONS.md` in the repository root. If present,
   read it for project-level conventions and CI check commands.

6. **Documentation files**: check for README files in `migration/` directory, and any
   architecture docs that describe the migration system.

7. **Test sibling analysis**: inspect `tests/api/advisory.rs` to understand test patterns
   for advisory-related functionality.

## Files to Create

### 1. `migration/src/m0002_drop_advisory_status/mod.rs` (NEW)

A new SeaORM migration module that drops the `status` column from the `advisory` table.
See `outputs/file-1-description.md` for detailed implementation.

## Files to Modify

### 2. `migration/src/lib.rs` (MODIFY)

Register the new migration module `m0002_drop_advisory_status` in the migrations list.
See `outputs/file-2-description.md` for detailed changes.

## Commit Message

The commit message follows Conventional Commits format and references TC-9205:

```
feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the unused status
column from the advisory table. The column was replaced by the severity
enum field in a previous migration and is no longer referenced by any
service or entity code.

Implements TC-9205
```

The commit will be created with the `--trailer` flag for AI attribution:

```bash
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the unused status
column from the advisory table. The column was replaced by the severity
enum field in a previous migration and is no longer referenced by any
service or entity code.

Implements TC-9205"
```

## Push and PR Creation (Step 10)

After committing, push the branch and create a PR targeting the feature branch TC-9005
(NOT main):

```bash
git push -u origin TC-9205
gh pr create --base TC-9005 --head TC-9205 \
  --title "feat(migration): drop deprecated status column from advisory table" \
  --body "## Summary

Add migration m0002_drop_advisory_status that removes the unused status column from the advisory table. The column was replaced by the severity enum field and is no longer referenced by any service or entity code.

### Changes
- Created \`migration/src/m0002_drop_advisory_status/mod.rs\` with up (drop column) and down (re-add column) methods
- Registered the new migration in \`migration/src/lib.rs\`

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)"
```

The `--base TC-9005` flag ensures the PR targets the feature branch, not main.

## Jira Updates (Step 11)

1. **Set Git Pull Request custom field** (`customfield_10875`) on TC-9205 with the PR URL in ADF format
2. **Add comment** to TC-9205 summarizing the changes made and including the PR link
3. **Transition** TC-9205 to **In Review**

## Self-Verification Checklist (Step 9)

Before committing, the following checks would be performed:

- **Scope containment**: `git diff --name-only` output must only include `migration/src/lib.rs` and the new `migration/src/m0002_drop_advisory_status/mod.rs`
- **Untracked file check**: verify `m0002_drop_advisory_status/mod.rs` is staged
- **Sensitive-pattern check**: scan diff for passwords, API keys, secrets
- **Documentation currency**: check if migration README or architecture docs need updating
- **Duplication check**: search for existing drop-column migrations to avoid duplication
- **Data-flow trace**: migration up drops column, down re-adds it -- both paths complete
- **Contract & sibling parity**: verify `MigrationTrait` is fully implemented (both `up` and `down`)
- **CI checks**: run any CI commands from CONVENTIONS.md, or fallback to `cargo test` and `cargo check`
