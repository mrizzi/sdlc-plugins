<!-- SYNTHETIC TEST DATA — task fixture with Target Branch set to a feature branch for implement-task eval testing -->

# Mock Jira Task

**Key**: TC-9205
**Summary**: Add migration to drop status table column
**Status**: To Do
**Labels**: ai-generated-jira
**Linked Issues**: is incorporated by TC-9005

---

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Add a database migration that drops the deprecated `status` column from the `advisory`
table. The column was replaced by the `severity` enum field in a previous migration and
is no longer read or written by any service code. Removing it reduces confusion and
prevents accidental usage.

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration list

## Files to Create
- `migration/src/m0002_drop_advisory_status/mod.rs` — migration that drops the `status` column from the `advisory` table

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` — implement `MigrationTrait` with `up` (drop column) and `down` (re-add column) methods
- The `advisory` entity in `entity/src/advisory.rs` no longer references the `status` column — verify this before proceeding
- Use SeaORM's `TableAlterStatement` to drop the column: `manager.alter_table(Table::alter().table(Advisory::Table).drop_column(Advisory::Status).to_owned()).await`
- Register the new migration in `migration/src/lib.rs` by adding it to the `vec![]` in the `migrations()` function, following the pattern of `m0001_initial`
- The `down` method should re-add the column as `ColumnDef::new(Advisory::Status).string().null()` to allow rollback

## Acceptance Criteria
- [ ] Migration drops the `status` column from the `advisory` table
- [ ] Migration `down` method re-adds the column as nullable string for rollback
- [ ] Migration is registered in `migration/src/lib.rs`
- [ ] No service or entity code references the `status` column

## Test Requirements
- [ ] Test that the migration runs successfully against a test database
- [ ] Test that the rollback (down) re-adds the column
- [ ] Verify that existing advisory queries still work after the column is dropped

## Dependencies
- Depends on: None
