# Implementation Plan for TC-9205: Add migration to drop status table column

## Task Summary

**Jira Issue:** TC-9205
**Summary:** Add a database migration that drops the deprecated `status` column from the `advisory` table.
**Repository:** trustify-backend
**Target Branch:** TC-9005 (feature branch, NOT main)
**Linked Issues:** is incorporated by TC-9005
**Dependencies:** None

## Target Branch Extraction

The **Target Branch** section specifies `TC-9005`. This is a feature branch (the parent feature issue ID), not `main`. All branch operations and the PR must target this feature branch.

## Branch Operations

1. **Checkout the target branch (TC-9005):**
   ```
   git checkout TC-9005
   git pull
   ```

2. **Create the task branch (TC-9205) from TC-9005:**
   ```
   git checkout -b TC-9205
   ```

   The task branch is named `TC-9205` (the task issue ID), which is distinct from `TC-9005` (the feature branch it is based on).

## Files to Inspect Before Modifying (Step 4 -- Understand the Code)

Before making any changes, inspect the following files using the Serena instance `serena_backend` (from the Repository Registry):

1. **`migration/src/m0001_initial/mod.rs`** -- Use `get_symbols_overview` to understand the existing migration pattern (how `MigrationTrait` is implemented, the `up` and `down` methods, how `TableAlterStatement` or `TableCreateStatement` is used). Then use `find_symbol` with `include_body=true` to read the `up` and `down` method bodies.

2. **`migration/src/lib.rs`** -- Use `get_symbols_overview` to see the `migrations()` function and how `m0001_initial` is registered in the `vec![]`. Read the full function body to understand the registration pattern.

3. **`entity/src/advisory.rs`** -- Verify that the `advisory` entity no longer references the `status` column. Use `get_symbols_overview` to see all fields/columns defined in the entity struct, then use `search_for_pattern` to search for any references to `Status` or `status` in the entity definition.

4. **Sibling analysis** -- Examine `m0001_initial/mod.rs` as the primary sibling for the new migration file. Also check `entity/src/sbom.rs` and `entity/src/package.rs` as sibling entity files for pattern comparison.

5. **Cross-codebase search** -- Use `search_for_pattern` (or Grep) to search the entire repository for any references to the `status` column on the `advisory` table, including service code, queries, and tests, to confirm no code still reads or writes this column.

6. **Documentation files** -- Check for `CONVENTIONS.md` at the repository root. Check `README.md` and `docs/architecture.md` for any references to the advisory schema.

7. **Test siblings** -- Examine `tests/api/advisory.rs` to understand integration test patterns (assertion style, setup, naming).

## Files to Modify

### 1. `migration/src/lib.rs`
- **Change:** Register the new migration module `m0002_drop_advisory_status` in the migration list.
- **Details:** Add `mod m0002_drop_advisory_status;` declaration and add `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` returned by the `migrations()` function, following the existing pattern of `m0001_initial`.

## Files to Create

### 1. `migration/src/m0002_drop_advisory_status/mod.rs`
- **Change:** Create a new migration module that drops the `status` column from the `advisory` table.
- **Details:** Implement `MigrationTrait` with:
  - `up` method: Uses `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await` to drop the column.
  - `down` method: Re-adds the column as `ColumnDef::new(Advisory::Status).string().null()` to allow rollback.
- **Pattern:** Follow the exact pattern from `m0001_initial/mod.rs` for struct definition, trait implementation, and SeaORM usage.

## Commit Message

```
refactor(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the unused status
column from the advisory table. The column was replaced by the severity
enum field in a previous migration and is no longer referenced by any
service or entity code.

Implements TC-9205
```

The commit command:
```
git commit --trailer="Assisted-by: Claude Code" -m "refactor(migration): drop deprecated status column from advisory table

Add migration m0002_drop_advisory_status that removes the unused status
column from the advisory table. The column was replaced by the severity
enum field in a previous migration and is no longer referenced by any
service or entity code.

Implements TC-9205"
```

## Push and PR Creation

1. **Push the task branch:**
   ```
   git push -u origin TC-9205
   ```

2. **Create PR targeting the feature branch TC-9005 (NOT main):**
   ```
   gh pr create --base TC-9005 --title "refactor(migration): drop deprecated status column from advisory table" --body "## Summary

   Add migration m0002_drop_advisory_status that drops the deprecated \`status\` column from the \`advisory\` table. The column was replaced by the \`severity\` enum field and is no longer read or written by any service code.

   ### Changes
   - Created \`migration/src/m0002_drop_advisory_status/mod.rs\` with \`up\` (drop column) and \`down\` (re-add as nullable string) methods
   - Registered the new migration in \`migration/src/lib.rs\`

   Implements [TC-9205](https://redhat.atlassian.net/browse/TC-9205)"
   ```

   The `--base TC-9005` flag ensures the PR targets the feature branch, not main.

## Verification Steps (Step 8 and 9)

1. **Acceptance Criteria verification:**
   - Confirm migration drops the `status` column (code inspection of `up` method)
   - Confirm `down` method re-adds the column as nullable string (code inspection)
   - Confirm migration is registered in `migration/src/lib.rs`
   - Confirm no service or entity code references the `status` column (grep/search)

2. **Scope containment:** Run `git diff --name-only` and verify only `migration/src/lib.rs` and `migration/src/m0002_drop_advisory_status/mod.rs` are changed/created.

3. **Sensitive-pattern check:** Search staged diff for secrets/credentials.

4. **Run tests:** `cargo test` to verify all tests pass.

5. **CI checks from CONVENTIONS.md:** If CONVENTIONS.md contains CI check commands, run them all.

## Jira Updates (Step 11)

1. Update the Git Pull Request custom field (`customfield_10875`) with the PR URL in ADF format.
2. Add a Jira comment with PR link, summary of changes, and confirmation of no deviations.
3. Transition TC-9205 to **In Review**.
