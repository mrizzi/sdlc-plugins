# Implementation Plan for TC-9205: Add migration to drop status table column

## Step 0 -- Validate Project Configuration

Verified the following sections exist in the project's CLAUDE.md (`claude-md-mock.md`):

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present, contains Project key (TC), Cloud ID, Feature issue type ID (10142), Git Pull Request custom field (customfield_10875), GitHub Issue custom field (customfield_10747)
3. **Code Intelligence** -- present, documents the `serena_backend` instance with rust-analyzer

All required sections verified. Proceeding.

## Step 1 -- Fetch and Parse Jira Task

Parsed task TC-9205 structured description:

| Section | Value |
|---|---|
| **Key** | TC-9205 |
| **Summary** | Add migration to drop status table column |
| **Repository** | trustify-backend |
| **Target Branch** | **TC-9005** |
| **Description** | Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code. |
| **Files to Modify** | `migration/src/lib.rs` |
| **Files to Create** | `migration/src/m0002_drop_advisory_status/mod.rs` |
| **Dependencies** | None |
| **Bookend Type** | Not present |
| **Target PR** | Not present |

### Target Branch extraction

The **Target Branch** section specifies `TC-9005`. This is a feature branch (not `main`), indicating a feature-branch workflow. The task branch will be created from this base, and the PR will target this branch.

### Linked Issues

The task is "incorporated by" TC-9005, confirming TC-9005 is the parent feature issue whose branch serves as the integration target.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 -- Transition to In Progress and Assign

Would perform:
1. `jira.user_info()` to get current user's account ID
2. `jira.edit_issue("TC-9205", assignee=<current-user-account-id>)` to assign
3. `jira.transition_issue("TC-9205")` to "In Progress"

## Step 4 -- Understand the Code (Inspection Before Modification)

### Files to inspect before making changes

1. **`migration/src/lib.rs`** (file to modify) -- Use `mcp__serena_backend__get_symbols_overview` to understand the current structure. Specifically need to see:
   - The `migrations()` function
   - How `m0001_initial` is registered in the `vec![]`
   - Module declarations (`mod m0001_initial;`)
   - Import statements

2. **`migration/src/m0001_initial/mod.rs`** (sibling migration, convention reference) -- Use `mcp__serena_backend__get_symbols_overview` then `mcp__serena_backend__find_symbol` with `include_body=true` to read the `MigrationTrait` implementation. This is the pattern to follow for the new migration.

3. **`entity/src/advisory.rs`** (entity file, verification) -- Use `mcp__serena_backend__get_symbols_overview` to verify that the `status` column is no longer referenced in the entity definition. The Implementation Notes state "The `advisory` entity in `entity/src/advisory.rs` no longer references the `status` column -- verify this before proceeding."

4. **`entity/src/lib.rs`** -- Quick check to understand entity module structure.

5. **`modules/fundamental/src/advisory/service/advisory.rs`** and **`modules/fundamental/src/advisory/model/summary.rs`** -- Verify no service or model code references the `status` column (Acceptance Criteria item 4).

### CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). Per the repo structure, `CONVENTIONS.md` exists at `trustify-backend/CONVENTIONS.md`. Would read it and extract:
- CI check commands (for Step 9)
- Code generation commands
- Naming rules, directory structure, code patterns, test conventions

### Convention conformance analysis

Sibling analysis targets:
- **`migration/src/m0001_initial/mod.rs`** -- the only existing sibling migration module. Examine its structure, naming, `MigrationTrait` implementation pattern, use of `Table::alter` vs `Table::create`, error handling approach.

### Documentation file identification

- `README.md` at repository root
- `CONVENTIONS.md` at repository root
- No API documentation directly related to migrations

## Step 5 -- Create Branch

### Branch operations (feature-branch workflow)

The Target Branch is **TC-9005** (not `main`). The task branch is named after the Jira issue ID **TC-9205** (not TC-9005).

```bash
git checkout TC-9005
git pull
git checkout -b TC-9205
```

This creates a new branch `TC-9205` from the feature branch `TC-9005`. The branch name is the task issue ID, distinct from the target/parent feature branch.

## Step 6 -- Implement Changes

### File 1: Create `migration/src/m0002_drop_advisory_status/mod.rs`

Create a new migration module following the pattern from `m0001_initial/mod.rs`. The migration implements `MigrationTrait` with:
- `up()` method: drops the `status` column from the `advisory` table using `TableAlterStatement`
- `down()` method: re-adds the `status` column as a nullable string for rollback

See `outputs/file-1-description.md` for full details.

### File 2: Modify `migration/src/lib.rs`

Register the new migration module:
1. Add `mod m0002_drop_advisory_status;` declaration
2. Add the migration to the `vec![]` in the `migrations()` function, following the pattern of `m0001_initial`

See `outputs/file-2-description.md` for full details.

## Step 7 -- Write Tests

Per the Test Requirements:
- Test that the migration runs successfully against a test database
- Test that the rollback (down) re-adds the column
- Verify that existing advisory queries still work after the column is dropped

Tests would be added to the migration test infrastructure or in `tests/api/advisory.rs`. See `outputs/file-3-description.md` for full details.

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| Migration drops the `status` column from the `advisory` table | The `up()` method uses `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await` |
| Migration `down` method re-adds the column as nullable string for rollback | The `down()` method uses `ColumnDef::new(Advisory::Status).string().null()` |
| Migration is registered in `migration/src/lib.rs` | Added to `mod` declarations and `vec![]` in `migrations()` |
| No service or entity code references the `status` column | Verified by inspecting `entity/src/advisory.rs`, `modules/fundamental/src/advisory/service/advisory.rs`, and grep for `status` references |

## Step 9 -- Self-Verification

### Scope containment
- `git diff --name-only` would show:
  - `migration/src/lib.rs` (in Files to Modify)
  - `migration/src/m0002_drop_advisory_status/mod.rs` (in Files to Create)
- Both files are in scope.

### Untracked file check
- `migration/src/m0002_drop_advisory_status/mod.rs` is a new file in a new directory -- would be flagged as untracked. Since it is listed in Files to Create and referenced by the modified `lib.rs`, it should be staged.

### Sensitive-pattern check
- No passwords, API keys, secrets, or `.env` references expected in migration code.

### Data-flow trace
- Migration `up()`: input (migration runner invocation) -> processing (ALTER TABLE DROP COLUMN) -> output (column removed from DB schema) -- COMPLETE
- Migration `down()`: input (rollback invocation) -> processing (ALTER TABLE ADD COLUMN) -> output (column re-added as nullable string) -- COMPLETE

### Contract & sibling parity
- `MigrationTrait` contract: requires `up()` and `down()` methods -- both implemented
- Sibling parity with `m0001_initial`: follows same `MigrationTrait` implementation pattern, same error handling, same module structure

## Step 10 -- Commit and Push

### Commit message

```bash
git add migration/src/m0002_drop_advisory_status/mod.rs
git add migration/src/lib.rs
git commit --trailer='Assisted-by: Claude Code' -m "feat(migration): drop deprecated status column from advisory table

Add m0002_drop_advisory_status migration that removes the unused status
column from the advisory table. The column was superseded by the severity
enum field and is no longer referenced by any entity or service code.
The down method re-adds the column as a nullable string for rollback.

Implements TC-9205"
```

Key points:
- Uses `--trailer='Assisted-by: Claude Code'` for AI attribution
- Conventional Commits format: `feat(migration): <description>`
- Footer references the Jira issue ID: `Implements TC-9205`

### Push and PR creation

```bash
git push -u origin TC-9205
gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "## Summary

Add database migration \`m0002_drop_advisory_status\` that drops the deprecated \`status\` column from the \`advisory\` table. The column was replaced by the \`severity\` enum field in a previous migration and is no longer read or written by any service code.

### Changes
- Created \`migration/src/m0002_drop_advisory_status/mod.rs\` with \`up\` (drop column) and \`down\` (re-add as nullable string) methods
- Registered the new migration in \`migration/src/lib.rs\`

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)"
```

Critical details:
- **Branch name**: `TC-9205` (the task issue ID)
- **PR base**: `--base TC-9005` (the Target Branch / parent feature branch, NOT main)
- **Push target**: `origin TC-9205`
- The PR targets the feature branch TC-9005, not main, because this is a feature-branch workflow

## Step 11 -- Update Jira

1. Update Git Pull Request custom field (`customfield_10875`) on TC-9205 with the PR URL in ADF format
2. Add a Jira comment with:
   - PR link
   - Summary: Created migration to drop deprecated `status` column from advisory table; registered in migration lib.rs
   - No deviations from plan
3. Transition TC-9205 to "In Review"
