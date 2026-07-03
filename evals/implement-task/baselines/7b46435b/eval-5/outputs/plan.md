# Implementation Plan for TC-9205: Add migration to drop status table column

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md contains all required sections:
- **Repository Registry**: present, lists `trustify-backend` with Serena instance `serena_backend` at path `./`
- **Jira Configuration**: present with Project key `TC`, Cloud ID, Feature issue type ID `10142`, Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`
- **Code Intelligence**: present with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` (rust-analyzer)

Validation passes. Proceed.

## Step 1 -- Fetch and Parse Jira Task

Parsed sections from TC-9205:

- **Repository**: trustify-backend
- **Target Branch**: TC-9005 (feature branch -- this is NOT main)
- **Description**: Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.
- **Files to Modify**: `migration/src/lib.rs` -- register the new migration module in the migration list
- **Files to Create**: `migration/src/m0002_drop_advisory_status/mod.rs` -- migration that drops the `status` column from the `advisory` table
- **Implementation Notes**: Follow existing migration pattern in `m0001_initial/mod.rs`, implement `MigrationTrait` with `up`/`down` methods, use SeaORM `TableAlterStatement`, register in `lib.rs` migrations vec
- **Acceptance Criteria**: 4 items (drop column, rollback re-adds, registered in lib.rs, no references to status column)
- **Test Requirements**: 3 items (migration runs, rollback works, existing queries still work)
- **Linked Issues**: is incorporated by TC-9005
- **Target PR**: not present
- **Bookend Type**: not present
- **Dependencies**: None

### Target Branch extraction

The Target Branch is `TC-9005`, which is a feature branch (not `main`). This means:
- The task branch will be created from the `TC-9005` feature branch
- The PR will target the `TC-9005` branch as its base

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

## Step 3 -- Transition to In Progress and Assign

Would perform:
1. `jira.user_info()` to get current user account ID
2. `jira.edit_issue(TC-9205, assignee=<account-id>)` to assign
3. `jira.transition_issue(TC-9205)` to In Progress

## Step 4 -- Understand the Code

### Files to inspect

1. **`migration/src/m0001_initial/mod.rs`** -- sibling migration to understand patterns (MigrationTrait implementation, up/down methods, SeaORM table operations)
2. **`migration/src/lib.rs`** -- understand migration registration pattern (the `migrations()` function returning `vec![]`)
3. **`entity/src/advisory.rs`** -- verify the `status` column is no longer referenced in the entity definition
4. **Advisory service and endpoint code** -- verify no service code references `status`:
   - `modules/fundamental/src/advisory/service/advisory.rs`
   - `modules/fundamental/src/advisory/model/summary.rs`
   - `modules/fundamental/src/advisory/model/details.rs`
   - `modules/fundamental/src/advisory/endpoints/list.rs`
   - `modules/fundamental/src/advisory/endpoints/get.rs`
5. **`modules/ingestor/src/graph/advisory/mod.rs`** -- verify ingestion code does not reference `status`
6. **`tests/api/advisory.rs`** -- sibling test file for test convention analysis

### CONVENTIONS.md lookup

Would check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). The repo structure shows it exists. Would read it for:
- CI check commands (verification commands extraction)
- Code generation commands
- Naming rules, directory structure, code patterns, test conventions

### Convention conformance analysis

Sibling analysis target: `migration/src/m0001_initial/mod.rs` -- the only existing migration module, serving as the pattern for the new migration.

### Documentation file identification

- `README.md` at repository root
- `CONVENTIONS.md` at repository root
- No migration-specific documentation identified in the repo structure

## Step 5 -- Create Branch (Feature Branch Workflow)

Since Target Branch is `TC-9005` (a feature branch), branch operations are:

```
git checkout TC-9005
git pull
git checkout -b TC-9205
```

This creates the task branch `TC-9205` from the feature branch `TC-9005`.

## Step 6 -- Implement Changes

### File 1: Create `migration/src/m0002_drop_advisory_status/mod.rs`

New migration module that:
- Implements `MigrationTrait` with `up` and `down` methods
- `up`: drops the `status` column from the `advisory` table using `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await`
- `down`: re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` for rollback
- Follows the exact pattern from `m0001_initial/mod.rs`
- Includes proper `use` imports for SeaORM migration types

### File 2: Modify `migration/src/lib.rs`

- Add `mod m0002_drop_advisory_status;` declaration
- Add `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, following the existing `m0001_initial` entry

## Step 7 -- Write Tests

Test the migration against the test database. Tests would be added in the migration crate or integration test suite. Based on the Test Requirements:

1. Test that the migration `up` runs successfully (column is dropped)
2. Test that the migration `down` runs successfully (column is re-added as nullable string)
3. Test that existing advisory queries (list, get) still work after migration

## Step 8 -- Verify Acceptance Criteria

1. Migration drops the `status` column -- verified by the `up` method implementation
2. Migration `down` re-adds as nullable string -- verified by the `down` method using `.string().null()`
3. Migration registered in `lib.rs` -- verified by the `mod` declaration and vec entry
4. No service/entity code references `status` -- verified by searching entity, service, endpoint, and ingestion code

## Step 9 -- Self-Verification

### Scope containment
- `migration/src/m0002_drop_advisory_status/mod.rs` -- in Files to Create (in scope)
- `migration/src/lib.rs` -- in Files to Modify (in scope)
- No out-of-scope files expected

### Sensitive-pattern check
- No passwords, API keys, secrets, or .env files involved

### Data-flow trace
- Migration up: drops column from advisory table -- no downstream data flow (destructive DDL operation)
- Migration down: re-adds column as nullable string -- allows rollback, no data restoration needed since column was deprecated and unused

### Contract & sibling parity
- `MigrationTrait` contract: requires `up` and `down` methods returning `Result<(), DbErr>` -- both implemented
- Sibling parity with `m0001_initial`: same struct pattern, same trait implementation, same async method signatures

## Step 10 -- Commit and Push

### Commit message

```
feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that removes the deprecated
`status` column from the advisory table. The column was replaced by
the `severity` enum field and is no longer referenced by any code.

The down method re-adds the column as a nullable string for rollback.

Implements TC-9205
```

With `--trailer="Assisted-by: Claude Code"`.

### Branch push and PR creation

Push to remote and create PR targeting the **TC-9005 feature branch** (not main):

```
git push -u origin TC-9205
gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "..."
```

The PR description would include:
- Summary of changes
- `Implements [TC-9205](<webUrl>)` with clickable Jira link
- GitHub issue reference (if the custom field had a value)

The `--base TC-9005` flag is critical -- it ensures the PR targets the feature branch, not main.

## Step 11 -- Update Jira

1. Update `customfield_10875` (Git Pull Request custom field) with the PR URL in ADF format
2. Add comment to TC-9205 with PR link, summary of changes, and any deviations
3. Transition TC-9205 to In Review
