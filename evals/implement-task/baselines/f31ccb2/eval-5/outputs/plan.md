# Implementation Plan: TC-9205 — Add migration to drop status table column

## Task Summary

Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code. Removing it reduces confusion and prevents accidental usage.

## Target Branch

The Target Branch extracted from the task description is **TC-9005** (a feature branch). This task is part of the feature-branch workflow -- it is incorporated by feature issue TC-9005, so the task branch targets the feature branch rather than `main`.

## Branch Operations

1. **Check out the target branch** (feature branch `TC-9005`):
   ```
   git checkout TC-9005
   git pull
   ```

2. **Create the task branch** from the feature branch:
   ```
   git checkout -b TC-9205
   ```
   The task branch is named after the Jira issue ID (`TC-9205`) per constraint 3.1. It is distinct from the target branch (`TC-9005`), which is the feature branch.

3. **PR targeting**: The PR must target the feature branch `TC-9005` (not `main`), because the task's Target Branch is `TC-9005`:
   ```
   gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "$(cat <<'EOF'
   ## Summary
   - Add `m0002_drop_advisory_status` migration that drops the deprecated `status` column from the `advisory` table
   - Register the new migration in `migration/src/lib.rs`
   - Include rollback support via `down()` that re-adds the column as a nullable string

   ## Jira
   Implements [TC-9205](https://jira.atlassian.net/browse/TC-9205)
   EOF
   )"
   ```
   This follows constraint 3.3: `gh pr create` MUST always specify `--base <target-branch>` matching the task's Target Branch value.

## Pre-Implementation Inspection

Before making any changes, the following files would be inspected (constraint 5.2 -- code MUST NOT be modified without first inspecting it):

1. **`migration/src/m0001_initial/mod.rs`** -- the existing migration sibling, to understand the pattern for `MigrationTrait` implementation, `up`/`down` methods, SeaORM imports, struct conventions, and identifier enum patterns
2. **`migration/src/lib.rs`** -- to understand how migrations are registered in the `migrations()` function and the module declaration pattern
3. **`entity/src/advisory.rs`** -- to verify the advisory entity no longer references the `status` column (acceptance criterion 4)
4. **`CONVENTIONS.md`** (if present) -- to check for project-specific coding conventions, CI check commands, and any migration-specific guidance

### Sibling Analysis

- **Primary sibling**: `migration/src/m0001_initial/mod.rs` would be read in full to discover:
  - How `MigrationTrait` is implemented (struct definition, `name()`, `up()`, `down()` methods)
  - Import patterns (which SeaORM types are imported, whether `prelude::*` is used)
  - Error handling patterns in migration methods
  - Module naming conventions for migration directories (`m<NNNN>_<snake_case_description>`)
  - Whether identifier enums (table/column names) are defined locally within the migration or imported from the entity crate
  - Whether `#[derive(DeriveMigrationName)]` or manual `name()` implementation is used
  - Whether `#[async_trait::async_trait]` attribute is present

### Pre-Implementation Verification

- Confirm that `entity/src/advisory.rs` does NOT contain a `Status` field or column reference
- Search service code (`modules/fundamental/src/advisory/`) for any remaining references to the `status` column on the advisory entity
- Search query code for advisory status references to satisfy acceptance criterion 4

## Files to Create

### 1. `migration/src/m0002_drop_advisory_status/mod.rs`

New migration module that drops the `status` column from the `advisory` table.

- Implements `MigrationTrait` with:
  - `name()` auto-derived via `#[derive(DeriveMigrationName)]`
  - `up()` dropping the `status` column using `Table::alter().table(Advisory::Table).drop_column(Advisory::Status)`
  - `down()` re-adding the column as `ColumnDef::new(Advisory::Status).string().null()` to allow rollback
- Defines a local `Advisory` enum with `#[derive(DeriveIden)]` for self-contained table/column identifiers

See `outputs/file-1-description.md` for full details.

## Files to Modify

### 2. `migration/src/lib.rs`

Register the new migration module:

- Add `mod m0002_drop_advisory_status;` module declaration alongside existing `mod m0001_initial;`
- Add `Box::new(m0002_drop_advisory_status::Migration)` to the `vec![]` in the `migrations()` function, after the existing `m0001_initial` entry to preserve chronological ordering

See `outputs/file-2-description.md` for full details.

## Commit Message

```
feat(migration): add migration to drop advisory status column

Add m0002_drop_advisory_status migration that removes the deprecated
status column from the advisory table. The column was replaced by the
severity enum field and is no longer referenced by any service or entity
code.

The down method re-adds the column as a nullable string for rollback
support.

Implements TC-9205
```

The commit command would include `--trailer="Assisted-by: Claude Code"` per constraint 2.3:
```
git commit --trailer="Assisted-by: Claude Code" -m "feat(migration): ..."
```

## Self-Verification Checks

1. **Scope containment** (constraint 1.4): Verify only `migration/src/lib.rs` and `migration/src/m0002_drop_advisory_status/mod.rs` are changed -- no unrelated files touched
2. **Sensitive pattern check**: Scan staged diff for secrets, credentials, or hardcoded values
3. **Data-flow trace** (constraint 5.6): Migration `up` drops the column, migration `down` re-adds it -- complete lifecycle covered
4. **Contract verification** (constraint 5.7): Verify `MigrationTrait` is fully implemented with all required methods (`name` via derive, `up`, `down`)
5. **Sibling parity** (constraint 5.8): Compare against `m0001_initial` for consistent patterns (error handling, import style, naming, derive macros)
6. **Entity verification**: Confirm `entity/src/advisory.rs` has no `status` column reference
7. **Service code verification**: Confirm no service code references `advisory.status`

## Acceptance Criteria Verification

- [ ] Migration drops the `status` column from the `advisory` table -- verified by inspecting `up()` method uses `drop_column(Advisory::Status)`
- [ ] Migration `down` method re-adds the column as nullable string for rollback -- verified by inspecting `down()` method uses `ColumnDef::new(Advisory::Status).string().null()`
- [ ] Migration is registered in `migration/src/lib.rs` -- verified by inspecting lib.rs module declaration and migrations() vec entry
- [ ] No service or entity code references the `status` column -- verified by grep search across entity and service code
