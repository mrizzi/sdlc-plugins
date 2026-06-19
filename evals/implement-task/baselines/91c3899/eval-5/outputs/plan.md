# Implementation Plan for TC-9205

## Task Summary

**Jira Issue**: TC-9205
**Summary**: Add migration to drop status table column
**Repository**: trustify-backend
**Target Branch**: TC-9005
**Linked Issues**: is incorporated by TC-9005 (feature branch)
**Dependencies**: None

## Step 0 -- Validate Project Configuration

The project CLAUDE.md contains all required sections:
- Repository Registry: trustify-backend with Serena instance `serena_backend`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence: Serena with rust-analyzer

Configuration is valid. Proceed.

## Step 1 -- Fetch and Parse Jira Task

### Parsed Sections

- **Repository**: trustify-backend
- **Target Branch**: TC-9005 (this is a feature branch, NOT main)
- **Description**: Add a database migration that drops the deprecated `status` column from the `advisory` table
- **Files to Modify**: `migration/src/lib.rs` -- register the new migration module
- **Files to Create**: `migration/src/m0002_drop_advisory_status/mod.rs` -- migration implementation
- **Implementation Notes**: Follow existing migration pattern in `m0001_initial/mod.rs`, use SeaORM `TableAlterStatement`
- **Acceptance Criteria**: 4 items (drop column, rollback, registration, no stale references)
- **Test Requirements**: 3 items (migration runs, rollback works, existing queries unaffected)
- **Bookend Type**: Not present
- **Target PR**: Not present

### Target Branch Extraction

The Target Branch is **TC-9005**. This is a feature branch (not main). The task branch will be created from this feature branch, and the PR will target this feature branch.

### GitHub Issue Extraction

The GitHub Issue custom field (customfield_10747) would be read from the Jira issue fields. If present, the GitHub issue reference would be included in the PR description.

## Step 1.5 -- Verify Description Integrity

Fetch issue comments via `jira.get_issue_comments(TC-9205)`. Look for digest comment starting with `[sdlc-workflow] Description digest:`. Compare stored digest against computed digest of the current description using `python3 scripts/sha256-digest.py`. Proceed or stop based on match.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user: `jira.user_info()`
2. Assign task: `jira.edit_issue(TC-9205, assignee=<current-user-account-id>)`
3. Transition: `jira.transition_issue(TC-9205) -> In Progress`

## Step 4 -- Understand the Code

### Code Inspection

Using Serena instance `serena_backend` (from Repository Registry):

1. **Inspect `migration/src/lib.rs`**: Use `mcp__serena_backend__get_symbols_overview` to understand the migration registration structure. Look for the `migrations()` function and the `vec![]` that lists migration modules.

2. **Inspect `migration/src/m0001_initial/mod.rs`**: Use `mcp__serena_backend__get_symbols_overview` and `mcp__serena_backend__find_symbol` with `include_body=true` to read the `MigrationTrait` implementation. This is the sibling migration file that establishes the pattern to follow.

3. **Inspect `entity/src/advisory.rs`**: Use `mcp__serena_backend__get_symbols_overview` to verify that the Advisory entity no longer references a `status` column. This confirms the column is safe to drop.

4. **Check for stale references**: Use `mcp__serena_backend__search_for_pattern` to search for `Advisory::Status` or `status` references in service code, endpoints, and models across the codebase.

5. **Documentation file identification**: Check for `CONVENTIONS.md` at repository root. Check for README files in `migration/` directory.

### CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root path `./CONVENTIONS.md`. The repo structure shows this file exists. Read it and extract:
- CI check commands (if any verification commands section exists)
- Code generation commands (if any)
- Naming rules, directory structure conventions, code patterns

### Convention Conformance Analysis

See `outputs/conventions.md` for full details. Key conventions discovered from sibling analysis of `m0001_initial/mod.rs`:
- Migration modules follow `m<NNNN>_<descriptive_name>/mod.rs` naming pattern
- Each migration implements `MigrationTrait` with `name()`, `up()`, and `down()` methods
- `up()` performs the forward migration, `down()` performs the rollback
- SeaORM manager is used for all DDL operations
- Migrations are registered in `lib.rs` by adding to the `vec![]` in `migrations()`

### Test Convention Analysis

- Integration tests in `tests/api/` use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Tests hit a real PostgreSQL test database
- Test naming follows `test_<endpoint>_<scenario>` pattern

## Step 5 -- Create Branch (Feature Branch Workflow)

This is the **default flow** (no Target PR, no Bookend Type).

The Target Branch is **TC-9005** (the feature branch). The task branch is named after the Jira issue ID **TC-9205**.

### Branch Operations

```bash
git checkout TC-9005
git pull
git checkout -b TC-9205
```

This checks out the feature branch TC-9005, pulls latest changes, then creates a new task branch TC-9205 from it. The task branch name is TC-9205 (the task issue ID), NOT TC-9005 (the feature branch).

## Step 6 -- Implement Changes

### File 1: `migration/src/m0002_drop_advisory_status/mod.rs` (CREATE)

New migration file that drops the `status` column from the `advisory` table. See `outputs/file-1-description.md` for detailed implementation.

### File 2: `migration/src/lib.rs` (MODIFY)

Register the new migration module in the migration list. See `outputs/file-2-description.md` for detailed changes.

## Step 7 -- Write Tests

Tests for the migration would be written per the Test Requirements:
- Test that the migration `up()` runs successfully against a test database
- Test that the rollback `down()` re-adds the column as a nullable string
- Verify that existing advisory queries still work after the column is dropped

These tests would follow the existing test conventions (assert_eq! pattern, real PostgreSQL test database).

## Step 8 -- Verify Acceptance Criteria

1. Migration drops the `status` column from the `advisory` table -- verified by `up()` implementation using `drop_column(Advisory::Status)`
2. Migration `down` method re-adds the column as nullable string for rollback -- verified by `down()` implementation using `ColumnDef::new(Advisory::Status).string().null()`
3. Migration is registered in `migration/src/lib.rs` -- verified by adding to the `vec![]` in `migrations()`
4. No service or entity code references the `status` column -- verified by codebase search in Step 4

## Step 9 -- Self-Verification

- **Scope containment**: `git diff --name-only` should show only `migration/src/lib.rs` and `migration/src/m0002_drop_advisory_status/mod.rs`
- **Untracked file check**: The new `mod.rs` file will be untracked; it is referenced by the modified `lib.rs` via `mod m0002_drop_advisory_status;` and must be staged
- **Sensitive-pattern check**: Search staged diff for secrets/credentials
- **CI checks from CONVENTIONS.md**: Run any extracted CI check commands
- **Duplication check**: Search for existing migration code that drops columns to ensure no duplication
- **Data-flow trace**: Migration is a standalone DDL operation; data flow is: migration runner -> up()/down() -> database schema change -- COMPLETE
- **Contract & sibling parity**: `MigrationTrait` implementation must include `name()`, `up()`, `down()` -- all present

## Step 10 -- Commit and Push

### Commit Message

```
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the unused status
column from the advisory table. The column was replaced by the severity
enum field in a previous migration and is no longer referenced by any
service or entity code. The down method re-adds the column as a nullable
string to support rollback.

Implements TC-9205"
```

### Push and PR Creation

```bash
git push -u origin TC-9205
gh pr create --base TC-9005 \
  --title "feat(migration): drop deprecated status column from advisory table" \
  --body "## Summary

- Add migration \`m0002_drop_advisory_status\` that drops the deprecated \`status\` column from the \`advisory\` table
- Register the new migration in \`migration/src/lib.rs\`
- Include rollback support (re-adds column as nullable string)

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)"
```

Key points:
- **Branch**: TC-9205 (task branch, created from TC-9005)
- **PR base**: `--base TC-9005` (targets the feature branch, NOT main)
- **Commit footer**: References TC-9205
- **Trailer**: `--trailer="Assisted-by: Claude Code"`

## Step 11 -- Update Jira

1. Update Git Pull Request custom field (customfield_10875) with PR URL in ADF format
2. Add comment to TC-9205 with PR link, summary of changes, and any deviations
3. Transition TC-9205 to In Review
