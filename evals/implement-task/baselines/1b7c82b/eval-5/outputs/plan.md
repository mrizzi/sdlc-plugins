# Implementation Plan: TC-9205 — Add migration to drop status table column

## Task Summary

Add a database migration that drops the deprecated `status` column from the `advisory` table. The column was replaced by the `severity` enum field in a previous migration and is no longer read or written by any service code.

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
   The task branch is named after the Jira issue ID per convention (constraint 3.1).

3. **PR targeting**: The PR must target the feature branch `TC-9005` (not `main`), because the task's Target Branch is `TC-9005`:
   ```
   gh pr create --base TC-9005 --title "feat(migration): add migration to drop advisory status column" --body "..."
   ```
   This follows constraint 3.3: `gh pr create` MUST always specify `--base <target-branch>` matching the task's Target Branch value.

## Pre-Implementation Inspection

Before making any changes, the following files would be inspected (constraint 5.2 — code MUST NOT be modified without first inspecting it):

1. **`migration/src/m0001_initial/mod.rs`** — the existing migration, to understand the pattern for `MigrationTrait` implementation, `up`/`down` methods, and SeaORM usage
2. **`migration/src/lib.rs`** — to understand how migrations are registered in the `migrations()` function
3. **`entity/src/advisory.rs`** — to verify the advisory entity no longer references the `status` column (acceptance criterion)
4. **`CONVENTIONS.md`** — to check for project-specific coding conventions and CI check commands

### Sibling Analysis

- **Sibling migration file**: `migration/src/m0001_initial/mod.rs` is the primary sibling. It would be read in full to discover:
  - How `MigrationTrait` is implemented (struct definition, `name()`, `up()`, `down()` methods)
  - Import patterns (which SeaORM types are imported)
  - Error handling patterns in migration methods
  - Module naming conventions for migration directories

### Verification Before Implementation

- Confirm that `entity/src/advisory.rs` does NOT contain a `Status` field or column reference
- Search service code (`modules/fundamental/src/advisory/`) for any remaining references to `status` on the advisory entity
- Search `modules/ingestor/src/graph/advisory/mod.rs` for `status` column references

## Files to Create

### 1. `migration/src/m0002_drop_advisory_status/mod.rs`

New migration module that drops the `status` column from the `advisory` table.

- Implements `MigrationTrait` with:
  - `name()` returning the migration identifier
  - `up()` dropping the `status` column using `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await`
  - `down()` re-adding the column as `ColumnDef::new(Advisory::Status).string().null()` for rollback support

## Files to Modify

### 2. `migration/src/lib.rs`

Register the new migration module:
- Add `mod m0002_drop_advisory_status;` declaration
- Add the migration to the `vec![]` in the `migrations()` function, following the pattern of `m0001_initial` registration

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

The commit would include `--trailer="Assisted-by: Claude Code"` per constraint 2.3.

## PR Description

```
## Summary
- Add `m0002_drop_advisory_status` migration that drops the deprecated `status` column from the `advisory` table
- Register the new migration in `migration/src/lib.rs`
- Include rollback support via `down()` that re-adds the column as a nullable string

## Jira
Implements [TC-9205](https://<jira-host>/browse/TC-9205)
```

## Self-Verification Checks

1. **Scope containment**: Verify only `migration/src/lib.rs` and `migration/src/m0002_drop_advisory_status/mod.rs` are changed
2. **Sensitive pattern check**: Scan staged diff for secrets/credentials
3. **Data-flow trace**: Migration up drops column, migration down re-adds it — complete lifecycle
4. **Contract verification**: Verify `MigrationTrait` is fully implemented (name, up, down methods)
5. **Sibling parity**: Compare against `m0001_initial` for consistent patterns (error handling, import style, naming)
6. **Entity verification**: Confirm `entity/src/advisory.rs` has no `status` column reference
7. **Service code verification**: Confirm no service code references `advisory.status`

## Acceptance Criteria Verification

- [ ] Migration drops the `status` column from the `advisory` table — verified by inspecting `up()` method
- [ ] Migration `down` method re-adds the column as nullable string for rollback — verified by inspecting `down()` method
- [ ] Migration is registered in `migration/src/lib.rs` — verified by inspecting lib.rs changes
- [ ] No service or entity code references the `status` column — verified by grep search across entity and service code
