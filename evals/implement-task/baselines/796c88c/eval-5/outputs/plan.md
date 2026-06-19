# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

**Jira Key:** TC-9205
**Summary:** Add a database migration that drops the deprecated `status` column from the `advisory` table.
**Repository:** trustify-backend
**Target Branch:** TC-9005 (feature branch for parent feature TC-9005)
**Linked Issues:** is incorporated by TC-9005
**Dependencies:** None

## Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains:
1. Repository Registry -- present, lists `trustify-backend` with Serena Instance `serena_backend` at path `./`
2. Jira Configuration -- present, includes Project key (TC), Cloud ID, Feature issue type ID, Git Pull Request custom field (`customfield_10875`), GitHub Issue custom field (`customfield_10747`)
3. Code Intelligence -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` using `rust-analyzer`

All sections are valid. Proceed.

## Step 1 -- Fetch and Parse Jira Task

Parsed fields from TC-9205:
- **Repository:** trustify-backend
- **Target Branch:** TC-9005
- **Description:** Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field and is no longer read or written.
- **Files to Modify:** `migration/src/lib.rs` -- register the new migration module
- **Files to Create:** `migration/src/m0002_drop_advisory_status/mod.rs` -- migration implementation
- **Implementation Notes:** Follow pattern in `m0001_initial/mod.rs`, implement `MigrationTrait`, use `TableAlterStatement` to drop column, register in `lib.rs`
- **Acceptance Criteria:** 4 items (drop column, rollback re-adds column, registered in lib.rs, no code references status column)
- **Test Requirements:** 3 items (migration runs, rollback works, existing queries work)
- **Bookend Type:** not present
- **Target PR:** not present
- **GitHub Issue:** check `customfield_10747` on the Jira issue (would be done via API)

## Step 1.5 -- Verify Description Integrity

Would fetch issue comments via `jira.get_issue_comments(TC-9205)`, locate digest comment, compute SHA-256 digest of description, and compare. Skipped in this eval (no external service calls).

## Step 2 -- Verify Dependencies

Task has no dependencies. Proceed.

## Step 3 -- Transition to In Progress and Assign

Would perform:
1. `jira.user_info()` to get current user's account ID
2. `jira.edit_issue(TC-9205, assignee=<account-id>)` to assign
3. `jira.transition_issue(TC-9205)` to "In Progress"

Skipped in this eval (no external service calls).

## Step 4 -- Understand the Code

### Code inspection

Using Serena instance `serena_backend` (via `mcp__serena_backend__<tool>`):

1. **`migration/src/lib.rs`**: Use `get_symbols_overview` to understand how migrations are registered. Expect a `migrations()` function returning `Vec<Box<dyn MigrationTrait>>` with `m0001_initial` currently listed.
2. **`migration/src/m0001_initial/mod.rs`**: Use `get_symbols_overview` and `find_symbol` with `include_body=true` to read the full migration implementation. This is the sibling file that serves as the pattern template.
3. **`entity/src/advisory.rs`**: Use `get_symbols_overview` to verify that the `Advisory` entity no longer references the `status` column. Confirm that `Advisory::Status` is still defined as a column enum variant (needed for the migration to reference it) but is not used in any active code.
4. **Cross-reference check**: Use `find_referencing_symbols` on `Advisory::Status` to confirm no service or entity code references the `status` column.
5. **Pattern search**: Use `search_for_pattern` to search for any string `"status"` in context of the `advisory` table across the codebase.

### CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at repository root (`./CONVENTIONS.md`). The repo structure lists it as present. Read it and extract:
- CI check commands (for Step 9)
- Code generation commands
- Any naming or structural conventions

### Convention conformance analysis

See `outputs/conventions.md` for the full list of discovered conventions from sibling analysis.

### Documentation file identification

- `README.md` at repository root
- `docs/architecture.md` and `docs/api.md` referenced in CLAUDE.md
- No migration-specific documentation identified

## Step 5 -- Create Branch

This is a default flow (no Target PR, no Bookend Type).

The Target Branch is `TC-9005` (the feature branch for the parent feature). The task branch is named after the Jira issue ID `TC-9205`.

```bash
git checkout TC-9005
git pull
git checkout -b TC-9205
```

This checks out the feature branch TC-9005 first, pulls the latest changes, then creates a new task branch TC-9205 from it. The PR will later target TC-9005, not main.

## Step 6 -- Implement Changes

### File 1: Create `migration/src/m0002_drop_advisory_status/mod.rs`

Create the new migration module following the pattern in `m0001_initial/mod.rs`. See `outputs/file-1-description.md` for detailed changes.

### File 2: Modify `migration/src/lib.rs`

Register the new migration module in the migrations list. See `outputs/file-2-description.md` for detailed changes.

## Step 7 -- Write Tests

Migration tests should be added to verify:
1. The migration runs successfully against a test database
2. The rollback (down) re-adds the column as a nullable string
3. Existing advisory queries still work after the column is dropped

See `outputs/file-3-description.md` for detailed test changes.

## Step 8 -- Verify Acceptance Criteria

1. Migration drops the `status` column from the `advisory` table -- verified by the `up()` method using `TableAlterStatement` to drop the column
2. Migration `down` method re-adds the column as nullable string for rollback -- verified by the `down()` method using `ColumnDef::new(Advisory::Status).string().null()`
3. Migration is registered in `migration/src/lib.rs` -- verified by adding `m0002_drop_advisory_status::Migration` to the migrations vec
4. No service or entity code references the `status` column -- verified via `find_referencing_symbols` and `search_for_pattern` in Step 4

## Step 9 -- Self-Verification

### Scope containment
- `git diff --name-only` should show only:
  - `migration/src/lib.rs` (modified -- listed in Files to Modify)
  - `migration/src/m0002_drop_advisory_status/mod.rs` (created -- listed in Files to Create)
- Any test files would be flagged as out-of-scope and require user approval

### Untracked file check
- Check `git status --short` for `??` entries in `migration/src/` directory
- The new `m0002_drop_advisory_status/mod.rs` should be staged

### Sensitive-pattern check
- Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`
- No secrets expected in migration code

### Documentation currency
- Migration does not change public APIs, configuration options, or setup steps
- No documentation updates needed

### CI checks from CONVENTIONS.md
- Run any CI check commands extracted from CONVENTIONS.md
- At minimum: `cargo build`, `cargo clippy`, `cargo fmt --check`
- Hard stop on any failure

### Data-flow trace
- Migration `up`: receives `SchemaManager` -> drops `status` column from `advisory` table -> returns `Ok(())` -- COMPLETE
- Migration `down`: receives `SchemaManager` -> adds `status` column back to `advisory` table as nullable string -> returns `Ok(())` -- COMPLETE
- Migration registration: `lib.rs` `migrations()` -> includes `m0002_drop_advisory_status::Migration` in vec -> returned to SeaORM migrator -- COMPLETE

### Contract & sibling parity
- `m0002_drop_advisory_status::Migration` implements `MigrationTrait`:
  - `name()` method: returns migration identifier string -- required by trait
  - `up()` method: applies forward migration -- required by trait
  - `down()` method: applies rollback -- required by trait
- Sibling parity with `m0001_initial::Migration`:
  - Both implement `MigrationTrait` with all required methods
  - Both use `SchemaManager` for database operations
  - Async trait methods match

### Duplication check
- No existing migration drops this column; no duplication expected

## Step 10 -- Commit and Push

### Commit message

```
feat(migration): drop deprecated status column from advisory table

Add migration m0002 that removes the unused `status` column from the
`advisory` table. The column was superseded by the `severity` enum field
and is no longer referenced by any service or entity code.

Implements TC-9205
```

With trailer:
```bash
git add migration/src/m0002_drop_advisory_status/mod.rs migration/src/lib.rs
git commit --trailer='Assisted-by: Claude Code' -m "feat(migration): drop deprecated status column from advisory table

Add migration m0002 that removes the unused status column from the
advisory table. The column was superseded by the severity enum field
and is no longer referenced by any service or entity code.

Implements TC-9205"
```

### Push and create PR

```bash
git push -u origin TC-9205
gh pr create --base TC-9005 --title "feat(migration): drop deprecated status column from advisory table" --body "## Summary

Add database migration m0002 that drops the deprecated \`status\` column from the \`advisory\` table. The column was replaced by the \`severity\` enum field in a previous migration and is no longer read or written by any service code.

### Changes
- Created \`migration/src/m0002_drop_advisory_status/mod.rs\` with \`MigrationTrait\` implementation
- Registered the new migration in \`migration/src/lib.rs\`
- \`up()\` drops the \`status\` column using \`TableAlterStatement\`
- \`down()\` re-adds the column as a nullable string for rollback

Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)"
```

Key points:
- The PR targets `TC-9005` (the feature branch), NOT `main`
- The task branch is `TC-9205`
- The `--base TC-9005` flag is explicitly specified
- The commit includes `--trailer='Assisted-by: Claude Code'`
- The commit message follows Conventional Commits with `feat(migration):` type/scope
- The commit footer references `Implements TC-9205`

## Step 11 -- Update Jira

Would perform (skipped in eval):
1. Update Git Pull Request custom field (`customfield_10875`) on TC-9205 with the PR URL in ADF format
2. Add comment to TC-9205 with PR link, summary of changes, and confirmation of no deviations
3. Transition TC-9205 to "In Review"
