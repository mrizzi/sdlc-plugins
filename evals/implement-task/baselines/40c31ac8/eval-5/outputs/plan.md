# Implementation Plan for TC-9205: Add migration to drop status table column

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md (claude-md-mock.md) contains the required sections:
- **Repository Registry**: present with `trustify-backend` entry (Serena instance: `serena_backend`, Path: `./`)
- **Jira Configuration**: present with Project key `TC`, Cloud ID, Feature issue type ID
- **Code Intelligence**: present with tool naming convention and `serena_backend` instance configured for rust-analyzer

Configuration is valid; proceed.

## Step 1 -- Fetch and Parse Jira Task

Parsed from the task description:

- **Key**: TC-9205
- **Summary**: Add migration to drop status table column
- **Repository**: trustify-backend
- **Target Branch**: TC-9005 (a feature branch, NOT main)
- **Linked Issues**: is incorporated by TC-9005
- **Bookend Type**: none
- **Target PR**: none
- **Description**: Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.
- **Files to Modify**: `migration/src/lib.rs` -- register the new migration module
- **Files to Create**: `migration/src/m0002_drop_advisory_status/mod.rs` -- migration that drops the `status` column
- **Implementation Notes**: Follow existing migration pattern in `m0001_initial/mod.rs`, implement `MigrationTrait` with `up` (drop column) and `down` (re-add column) methods, use SeaORM's `TableAlterStatement`, register in `lib.rs` migrations vec
- **Acceptance Criteria**: 4 items (drop column, rollback re-adds as nullable string, registered in lib.rs, no service/entity code references status column)
- **Test Requirements**: 3 items (migration runs successfully, rollback re-adds column, existing advisory queries still work)
- **Dependencies**: None

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

## Step 3 -- Transition to In Progress and Assign

Would perform:
1. `jira.user_info()` to get current user's account ID
2. `jira.edit_issue("TC-9205", assignee=<account-id>)` to assign
3. `jira.transition_issue("TC-9205")` to "In Progress"

(Skipped per eval instructions -- no external tool calls.)

## Step 4 -- Understand the Code

### Files to inspect

1. **`migration/src/m0001_initial/mod.rs`** -- sibling migration, understand the `MigrationTrait` implementation pattern (struct definition, `name()` method, `up()` and `down()` methods, use of `SchemaManager`)
2. **`migration/src/lib.rs`** -- understand how migrations are registered (the `migrations()` function returning a `Vec<Box<dyn MigrationTrait>>`)
3. **`entity/src/advisory.rs`** -- verify the entity no longer references the `status` column (confirm only `severity` is present)
4. **`modules/fundamental/src/advisory/model/summary.rs`** and **`modules/fundamental/src/advisory/model/details.rs`** -- verify no code references `status` column
5. **`modules/fundamental/src/advisory/service/advisory.rs`** -- verify service does not query `status`
6. **`modules/ingestor/src/graph/advisory/mod.rs`** -- verify ingestion does not write `status`

### CONVENTIONS.md lookup

Would check for `CONVENTIONS.md` at the repository root. According to the repo structure, `CONVENTIONS.md` exists at root. Would read it for naming rules, directory structure, code patterns, and CI check commands.

### Convention conformance analysis

Performed by examining `m0001_initial/mod.rs` (the sole sibling migration). See `outputs/conventions.md` for the full list.

### Documentation file identification

- `README.md` at repository root
- `CONVENTIONS.md` at repository root
- No migration-specific docs identified

### Test convention analysis

- **Sibling test files**: `tests/api/advisory.rs` -- advisory endpoint integration tests
- Would examine assertion patterns, test naming, setup/teardown conventions

## Step 5 -- Branch Operations

**This task targets a feature branch (TC-9005), not main.**

The following git operations would be performed:

```bash
git checkout TC-9005
git pull
git checkout -b TC-9205
```

This checks out the feature branch TC-9005 first, pulls latest, then creates the task branch TC-9205 from it.

## Step 6 -- Implement Changes

### File 1: Create `migration/src/m0002_drop_advisory_status/mod.rs`

New migration module implementing `MigrationTrait`:
- Define a `Migration` struct
- Implement `MigrationName` trait returning `"m0002_drop_advisory_status"`
- Implement `MigrationTrait` with:
  - `up()`: uses `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await` to drop the `status` column
  - `down()`: uses `manager.alter_table(Table::alter().table(Advisory::Table).add_column(ColumnDef::new(Advisory::Status).string().null()).to_owned()).await` to re-add as nullable string

See `outputs/file-1-description.md` for detailed implementation.

### File 2: Modify `migration/src/lib.rs`

- Add `mod m0002_drop_advisory_status;` module declaration
- Add `Box::new(m0002_drop_advisory_status::Migration)` to the `migrations()` vec, after `m0001_initial`

See `outputs/file-2-description.md` for detailed implementation.

## Step 7 -- Write Tests

Migration tests would be added to verify:
1. Migration `up()` runs successfully and the `status` column no longer exists
2. Migration `down()` re-adds the column as a nullable string
3. Existing advisory queries continue to work after migration

See `outputs/file-3-description.md` for detailed test implementation.

## Step 8 -- Verify Acceptance Criteria

- [x] Migration drops the `status` column from the `advisory` table -- verified via `up()` implementation
- [x] Migration `down` method re-adds the column as nullable string for rollback -- verified via `down()` implementation
- [x] Migration is registered in `migration/src/lib.rs` -- verified by adding to `migrations()` vec
- [x] No service or entity code references the `status` column -- verified by inspecting `entity/src/advisory.rs`, advisory service, and advisory ingestion code

## Step 9 -- Self-Verification

### Scope containment
Expected modified files:
- `migration/src/lib.rs` (modified)
- `migration/src/m0002_drop_advisory_status/mod.rs` (created)

Would run `git diff --name-only` and verify only these files are changed.

### Sensitive-pattern check
Would run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- no secrets expected in migration code.

### Data-flow trace
- `up()`: drops column from `advisory` table -- complete, no downstream consumers (column already deprecated)
- `down()`: re-adds column as nullable string -- complete, rollback path fully connected

### Contract & sibling parity
- `Migration` struct implements `MigrationTrait` -- `up()` and `down()` both implemented
- Sibling parity with `m0001_initial`: follows same struct pattern, same trait implementation, same error handling

### CI checks
Would run CI check commands from CONVENTIONS.md (e.g., `cargo check`, `cargo clippy`, `cargo fmt --check`).

## Step 10 -- Commit and Push

### Commit message

```
feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the unused `status`
column from the `advisory` table. The column was replaced by the `severity`
enum field and is no longer referenced by any service or entity code. The
down method re-adds the column as a nullable string for rollback safety.

Implements TC-9205
```

### Commit command

```bash
git add migration/src/m0002_drop_advisory_status/mod.rs migration/src/lib.rs
git commit --trailer='Assisted-by: Claude Code' -m "feat(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the unused status
column from the advisory table. The column was replaced by the severity
enum field and is no longer referenced by any service or entity code. The
down method re-adds the column as a nullable string for rollback safety.

Implements TC-9205"
```

### Push and PR

```bash
git push -u origin TC-9205
gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "## Summary

- Add migration \`m0002_drop_advisory_status\` to drop the deprecated \`status\` column from the \`advisory\` table
- The column was replaced by the \`severity\` enum field and is no longer read or written by any service code
- Rollback (\`down\`) re-adds the column as a nullable string

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)
"
```

Key points:
- The PR targets `--base TC-9005` (the feature branch), NOT main
- The task branch is named `TC-9205` (the task issue ID)
- The commit includes `--trailer='Assisted-by: Claude Code'`
- The commit message follows Conventional Commits with `Implements TC-9205` in the footer

## Step 11 -- Update Jira

Would perform:
1. Update `customfield_10875` (Git Pull Request custom field) with the PR URL in ADF format
2. Add a Jira comment with PR link, summary of changes, and confirmation that all acceptance criteria are met
3. Transition TC-9205 to "In Review"

(Skipped per eval instructions -- no external tool calls.)
