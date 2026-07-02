# Implementation Plan for TC-9205: Add migration to drop status table column

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md (claude-md-mock.md) contains all required sections:

1. **Repository Registry** -- present with `trustify-backend` entry, Serena instance `serena_backend`, path `./`
2. **Jira Configuration** -- present with Project key `TC`, Cloud ID, Feature issue type ID `10142`, Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`
3. **Code Intelligence** -- present with tool naming convention `mcp__<serena-instance>__<tool>`, configured instance `serena_backend` with `rust-analyzer`

Validation passes. Proceed.

## Step 1 -- Fetch and Parse Jira Task

Parsed sections from the task description:

- **Repository**: trustify-backend
- **Target Branch**: TC-9005 (a feature branch, not main)
- **Description**: Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.
- **Files to Modify**: `migration/src/lib.rs` -- register the new migration module
- **Files to Create**: `migration/src/m0002_drop_advisory_status/mod.rs` -- migration that drops the `status` column
- **Implementation Notes**: Follow the existing migration pattern in `m0001_initial/mod.rs`, use SeaORM `TableAlterStatement`, register in `lib.rs` migrations vec
- **Acceptance Criteria**: 4 items (drop column, down method re-adds, registered in lib.rs, no references to status column)
- **Test Requirements**: 3 items (migration runs, rollback works, existing queries still work)
- **Dependencies**: None
- **Target PR**: Not present (default flow)
- **Bookend Type**: Not present (default flow)
- **Linked Issues**: is incorporated by TC-9005

### Target Branch extraction

The Target Branch is **TC-9005**. This is a feature branch (not `main`). The task branch will be created from TC-9005, and the PR will target `--base TC-9005`.

## Step 1.5 -- Verify Description Integrity

Would fetch comments via `jira.get_issue_comments(TC-9205)` and look for a `[sdlc-workflow] Description digest:` comment. Compare the stored digest against a freshly computed digest of the description using `python3 scripts/sha256-digest.py`. Proceed or stop based on match/mismatch.

## Step 2 -- Verify Dependencies

The task lists "Depends on: None". No dependency verification needed.

## Step 3 -- Transition to In Progress and Assign

1. Call `jira.user_info()` to get current user's account ID
2. Call `jira.edit_issue(TC-9205, assignee=<account-id>)` to assign
3. Call `jira.transition_issue(TC-9205, "In Progress")` to transition

## Step 4 -- Understand the Code

### Code inspection

Using the Serena instance `serena_backend` (tool prefix: `mcp__serena_backend__`):

1. **Inspect `migration/src/lib.rs`**: Use `mcp__serena_backend__get_symbols_overview` to see the structure -- expect a `migrations()` function returning `Vec<Box<dyn MigrationTrait>>` with `m0001_initial` registered.
2. **Inspect `migration/src/m0001_initial/mod.rs`**: Use `mcp__serena_backend__find_symbol` with `include_body=true` to read the `MigrationTrait` implementation -- understand the `up()` and `down()` method patterns, how `Table::alter()` or `Table::create()` is used, and the import structure.
3. **Inspect `entity/src/advisory.rs`**: Use `mcp__serena_backend__get_symbols_overview` to verify the Advisory entity no longer references a `Status` column -- confirm only `Severity` and other fields are present. Also use `mcp__serena_backend__find_referencing_symbols` on the Advisory entity to check for any remaining references to `status`.
4. **Search for status column references**: Use `mcp__serena_backend__search_for_pattern` with pattern `Advisory::Status` or `status` in the context of advisory queries across `modules/` and `entity/` to confirm no service code references it.

### CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). The repository structure shows it exists. Read it and extract:
- Any CI check commands (formatting, linting, compilation) for use in Step 9
- Any code generation commands
- Naming rules, directory structure conventions, migration conventions

### Convention conformance analysis (sibling analysis)

**Sibling file for migration**: `migration/src/m0001_initial/mod.rs` is the only existing migration and serves as the sibling for `m0002_drop_advisory_status/mod.rs`.

Inspect `m0001_initial/mod.rs` for:
- Module structure (single `mod.rs` file implementing `MigrationTrait`)
- Naming conventions for migration modules (`m<NNNN>_<description>`)
- Import organization (`use sea_orm_migration::prelude::*`)
- How the `Migration` struct is defined (unit struct)
- `up()` and `down()` method signatures and patterns
- How table/column identifiers are referenced (e.g., `Advisory::Table`, `Advisory::Status`)
- Error handling (`Result<(), DbErr>`)

**Sibling file for lib.rs registration**: The existing `lib.rs` pattern shows how migrations are imported and added to the vec.

### Test convention analysis

**Sibling test files**: `tests/api/advisory.rs` is the closest test file for advisory-related functionality. Inspect for:
- Assertion style (`assert_eq!` with `StatusCode`)
- Test naming conventions
- Database setup/teardown patterns
- How migration tests are structured (if any exist)

### Documentation file identification

- `README.md` at repository root
- `CONVENTIONS.md` at repository root
- No migration-specific documentation files identified in the tree

## Step 5 -- Create Branch (Feature Branch Flow)

Since the Target Branch is **TC-9005** (not main), the branch operations are:

```bash
git checkout TC-9005
git pull
git checkout -b TC-9205
```

This creates task branch `TC-9205` from the feature branch `TC-9005`. The task branch name matches the Jira issue ID (TC-9205), which is distinct from the feature branch TC-9005.

## Step 6 -- Implement Changes

### Files to Create

#### 1. `migration/src/m0002_drop_advisory_status/mod.rs`

Create a new migration module that:
- Implements `MigrationTrait` for a unit struct `Migration`
- `up()` method: drops the `status` column from the `advisory` table using `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await`
- `down()` method: re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` for rollback
- Follows the exact pattern from `m0001_initial/mod.rs`
- Includes proper documentation comments on the struct and methods

### Files to Modify

#### 2. `migration/src/lib.rs`

- Add `mod m0002_drop_advisory_status;` declaration
- Add `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, after the existing `m0001_initial` entry

## Step 7 -- Write Tests

Implement tests per the Test Requirements:
- Test that the migration runs successfully against a test database
- Test that the rollback (down) re-adds the column
- Verify that existing advisory queries still work after the column is dropped

These would likely be added to `tests/api/advisory.rs` or a dedicated migration test file, following the project's test conventions.

## Step 8 -- Verify Acceptance Criteria

1. Migration drops the `status` column from the `advisory` table -- verified by the `up()` implementation
2. Migration `down` method re-adds the column as nullable string for rollback -- verified by the `down()` implementation
3. Migration is registered in `migration/src/lib.rs` -- verified by the lib.rs modification
4. No service or entity code references the `status` column -- verified by the search in Step 4

## Step 9 -- Self-Verification

### Scope containment
Run `git diff --name-only` and confirm only these files are modified/created:
- `migration/src/lib.rs` (modified)
- `migration/src/m0002_drop_advisory_status/mod.rs` (created)

Any additional files would need user approval.

### Untracked file check
Run `git status --short` to find untracked files in the `migration/src/` directory. Flag any that are referenced by code.

### Sensitive-pattern check
Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` to ensure no secrets are staged.

### CI checks from CONVENTIONS.md
Run all CI check commands extracted from CONVENTIONS.md (e.g., `cargo fmt --check`, `cargo clippy`, `cargo build`).

### Data-flow trace
- Migration `up()`: input (migration runner) -> process (drop column via ALTER TABLE) -> output (column removed from DB) -- COMPLETE
- Migration `down()`: input (migration runner) -> process (add column via ALTER TABLE) -> output (column restored in DB) -- COMPLETE
- Registration: `lib.rs` vec includes new migration -> migration runner discovers it -- COMPLETE

### Contract & sibling parity
- `Migration` struct implements `MigrationTrait` -- verify `up()` and `down()` both return `Result<(), DbErr>` and match the trait signature
- Sibling parity with `m0001_initial::Migration` -- both implement the same trait with the same patterns

## Step 10 -- Commit and Push

### Commit message

```
refactor(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the status column
from the advisory table. The column was replaced by the severity enum
field in a previous migration and is no longer referenced by any service
or entity code.

The down method re-adds the column as a nullable string to support
rollback.

Implements TC-9205
```

With trailer: `--trailer="Assisted-by: Claude Code"`

### Push and create PR

```bash
git push -u origin TC-9205
```

```bash
gh pr create --base TC-9005 \
  --title "refactor(migration): drop deprecated status column from advisory table" \
  --body "## Summary

- Add migration \`m0002_drop_advisory_status\` to drop the deprecated \`status\` column from the \`advisory\` table
- Register the new migration in \`migration/src/lib.rs\`
- Include rollback support (re-adds column as nullable string)

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)
"
```

Key: the PR targets `--base TC-9005` (the feature branch), NOT `--base main`.

## Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) on TC-9205 with the PR URL using ADF format
2. **Add comment** to TC-9205 with:
   - PR link
   - Summary of changes: added migration to drop status column, registered in lib.rs, rollback support included
   - No deviations from the plan
   - Footer with sdlc-workflow version from plugin.json
3. **Transition** TC-9205 to "In Review"

## Branch Operations Summary

| Operation | Command |
|---|---|
| Checkout target branch | `git checkout TC-9005` |
| Pull latest | `git pull` |
| Create task branch | `git checkout -b TC-9205` |
| Push task branch | `git push -u origin TC-9205` |
| Create PR | `gh pr create --base TC-9005 ...` |

The PR targets TC-9005 (the feature branch), not main. The task branch TC-9205 is distinct from the feature branch TC-9005.
