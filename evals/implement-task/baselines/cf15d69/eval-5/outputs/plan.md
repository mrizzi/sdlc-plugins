# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

**Jira Issue**: TC-9205
**Summary**: Add migration to drop status table column
**Repository**: trustify-backend
**Target Branch**: TC-9005 (feature branch, NOT main)
**Parent Feature**: TC-9005 (linked via "is incorporated by")
**Dependencies**: None

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md (`claude-md-mock.md`) contains all required sections:
1. **Repository Registry** -- present, lists `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present, includes Project key (TC), Cloud ID, Feature issue type ID (10142)
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and `serena_backend` configured with `rust-analyzer`

Validation passes. Proceed.

## Step 1 -- Fetch and Parse Jira Task

Parsed sections from the task description:

- **Repository**: trustify-backend
- **Target Branch**: TC-9005
- **Description**: Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.
- **Files to Modify**: `migration/src/lib.rs` -- register the new migration module
- **Files to Create**: `migration/src/m0002_drop_advisory_status/mod.rs` -- migration that drops the `status` column
- **Implementation Notes**: Follow existing migration pattern in `m0001_initial/mod.rs`, implement `MigrationTrait` with `up`/`down`, use SeaORM `TableAlterStatement`, register in `lib.rs`
- **Acceptance Criteria**: Migration drops column, down re-adds as nullable string, migration registered, no code references status column
- **Test Requirements**: Migration runs successfully, rollback re-adds column, existing queries still work
- **Bookend Type**: not present
- **Target PR**: not present
- **Dependencies**: None

**GitHub Issue extraction**: Check `customfield_10747` on the fetched issue. If present, extract and store the reference for use in PR description.

## Step 1.5 -- Verify Description Integrity

Fetch comments on TC-9205 via `jira.get_issue_comments("TC-9205")`. Search for comment starting with `[sdlc-workflow] Description digest:`. Compare stored digest with computed digest of current description. Proceed based on match/mismatch/absence.

## Step 2 -- Verify Dependencies

No dependencies listed. Skip.

## Step 3 -- Transition to In Progress and Assign

1. `jira.user_info()` -- get current user's account ID
2. `jira.edit_issue("TC-9205", assignee=<account-id>)` -- assign task
3. `jira.transition_issue("TC-9205")` -- transition to "In Progress"

## Step 4 -- Understand the Code (Pre-Implementation Inspection)

### 4.1 Inspect files to modify

Using the Serena instance `serena_backend` (tools called as `mcp__serena_backend__<tool>`):

1. **`migration/src/lib.rs`**: Use `mcp__serena_backend__get_symbols_overview` to understand the current structure -- specifically the `migrations()` function and how `m0001_initial` is registered in the `vec![]`.
2. **`migration/src/m0001_initial/mod.rs`**: Use `mcp__serena_backend__get_symbols_overview` to understand the existing migration pattern -- struct name, `MigrationTrait` implementation, `up()` and `down()` methods, imports used.

### 4.2 Verify entity code

Use `mcp__serena_backend__get_symbols_overview` on `entity/src/advisory.rs` to confirm the `status` column is NOT referenced in the entity definition (the task states it was already removed and replaced by `severity`).

Use `mcp__serena_backend__search_for_pattern` or Grep to search for any remaining references to `Advisory::Status` or `status` column across the codebase (entity, service, endpoint, and test code) to confirm no code depends on it.

### 4.3 Convention conformance analysis (siblings)

Identify sibling files for each file being modified or created:

- **For `migration/src/m0002_drop_advisory_status/mod.rs`** (new file): The sibling is `migration/src/m0001_initial/mod.rs`. Inspect it with `mcp__serena_backend__get_symbols_overview` and `mcp__serena_backend__find_symbol` (with `include_body=true`) to understand:
  - Struct naming convention (e.g., `Migration`)
  - Import patterns (SeaORM prelude, entity references)
  - `MigrationTrait` implementation structure
  - `up()` and `down()` method patterns
  - `name()` method return value format
  - Error handling approach

- **For `migration/src/lib.rs`** (modify): Already inspected above. Understand how migrations are registered.

### 4.4 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). The repo structure shows `CONVENTIONS.md` exists. Read it to extract:
- Project-level conventions (naming, patterns, structure)
- CI check commands (if any) for use in Step 9
- Code generation commands (if any)

### 4.5 Test convention analysis

For test files, identify sibling test files in `tests/api/` (e.g., `advisory.rs`, `sbom.rs`). Use `mcp__serena_backend__get_symbols_overview` on 2-3 test files to understand:
- Test setup patterns (database seeding, test fixtures)
- Assertion style (`assert_eq!` with `StatusCode`)
- Test naming conventions
- Migration test patterns (if any exist)

### 4.6 Documentation file identification

Identify related documentation:
- `README.md` at repo root
- `CONVENTIONS.md` at repo root
- `docs/architecture.md` and `docs/api.md` (from CLAUDE.md references)

Record these for documentation impact evaluation in Step 6.

## Step 5 -- Branch Operations

Check out the **Target Branch** `TC-9005` (NOT main), pull latest, and create a task branch:

```bash
git checkout TC-9005
git pull
git checkout -b TC-9205
```

The task branch is named `TC-9205` (the task issue ID), distinct from the target branch `TC-9005`.

## Step 6 -- Implement Changes

### File 1: CREATE `migration/src/m0002_drop_advisory_status/mod.rs`

Create the new migration module following the pattern discovered from `m0001_initial/mod.rs`:

- Define a migration struct (e.g., `Migration`)
- Implement `MigrationTrait` with:
  - `name()` returning a descriptive migration name
  - `up()` using `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await` to drop the `status` column
  - `down()` using `manager.alter_table(Table::alter().table(Advisory::Table).add_column(ColumnDef::new(Advisory::Status).string().null()).to_owned()).await` to re-add the column as a nullable string for rollback
- Include proper imports from SeaORM and entity crate
- Add documentation comments on the struct and methods

### File 2: MODIFY `migration/src/lib.rs`

- Add `mod m0002_drop_advisory_status;` declaration
- Add `Box::new(m0002_drop_advisory_status::Migration)` (or equivalent based on the pattern found in the existing `vec![]`) to the `migrations()` function, after `m0001_initial`

### Documentation impact

Evaluate whether `README.md`, `docs/architecture.md`, or `docs/api.md` need updating. Since this is a migration that removes an internal column (not a public API or configuration change), documentation updates are unlikely to be needed.

## Step 7 -- Write Tests

Implement tests based on Test Requirements:

- Test that the migration runs successfully against a test database
- Test that the rollback (down) re-adds the column
- Verify that existing advisory queries still work after the column is dropped

Follow the test conventions discovered from sibling test files in `tests/api/`. Each test function will have a `///` doc comment explaining what it verifies and given-when-then section comments for non-trivial tests.

## Step 8 -- Verify Acceptance Criteria

Verify each criterion:
1. Migration drops the `status` column from the `advisory` table -- confirmed by `up()` implementation
2. Migration `down` method re-adds the column as nullable string for rollback -- confirmed by `down()` implementation
3. Migration is registered in `migration/src/lib.rs` -- confirmed by `lib.rs` modification
4. No service or entity code references the `status` column -- confirmed by codebase search in Step 4

## Step 9 -- Self-Verification

### Scope containment
Run `git diff --name-only` and verify only these files are modified/created:
- `migration/src/lib.rs` (modified)
- `migration/src/m0002_drop_advisory_status/mod.rs` (created)

Any out-of-scope files require user approval.

### Untracked file check
Run `git status --short`, filter `??` entries by proximity to modified directories, search for code references to any flagged untracked files.

### Sensitive-pattern check
Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` to catch secrets.

### Documentation currency
Verify that no documentation files describe the `status` column behavior that needs updating.

### CI checks from CONVENTIONS.md
Run any CI check commands extracted from `CONVENTIONS.md` in Step 4. If any fail, stop and fix before proceeding.

### Data-flow trace
- Migration `up()` -> drops `status` column from `advisory` table -> COMPLETE (no downstream consumers since entity already updated)
- Migration `down()` -> re-adds `status` column as nullable string -> COMPLETE (rollback path)
- Migration registration in `lib.rs` -> migration runner picks up new migration -> COMPLETE

### Contract & sibling parity
- `Migration` struct implements `MigrationTrait` -- verify `name()`, `up()`, `down()` are all implemented per the trait contract
- Sibling parity with `m0001_initial::Migration` -- verify same import patterns, error handling, method signatures

### Duplication check
Search for any existing migration that drops columns from `advisory` to avoid duplication.

## Step 10 -- Commit and Push

### Commit message

```
feat(migration): drop deprecated status column from advisory table

The status column was replaced by the severity enum field in a previous
migration and is no longer read or written by any service code. Removing
it reduces confusion and prevents accidental usage.

Implements TC-9205
```

### Commit command

```bash
git add migration/src/m0002_drop_advisory_status/mod.rs migration/src/lib.rs
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): drop deprecated status column from advisory table

The status column was replaced by the severity enum field in a previous
migration and is no longer read or written by any service code. Removing
it reduces confusion and prevents accidental usage.

Implements TC-9205"
```

### Push and create PR

```bash
git push -u origin TC-9205
gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "## Summary

- Adds migration \`m0002_drop_advisory_status\` that drops the deprecated \`status\` column from the \`advisory\` table
- Implements rollback support via \`down()\` method that re-adds the column as a nullable string
- Registers the new migration in \`migration/src/lib.rs\`

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)
"
```

**Key**: The PR targets `TC-9005` via `--base TC-9005`, NOT main. This is because the Target Branch specified in the task is `TC-9005` (the parent feature branch).

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field** (`customfield_10875`) on TC-9205 with the PR URL in ADF format (inlineCard)
2. **Add comment** to TC-9205 with:
   - PR link
   - Summary: Added migration `m0002_drop_advisory_status` to drop the deprecated `status` column from the `advisory` table. Implemented `up()` (drop column) and `down()` (re-add as nullable string) methods. Registered migration in `lib.rs`.
   - No deviations from the plan.
   - Comment footer with sdlc-workflow version from `plugin.json`
3. **Transition** TC-9205 to "In Review"

## Files Summary

| File | Action | Description |
|---|---|---|
| `migration/src/m0002_drop_advisory_status/mod.rs` | CREATE | New migration module that drops the `status` column from `advisory` |
| `migration/src/lib.rs` | MODIFY | Register the new migration module in the migrations list |
