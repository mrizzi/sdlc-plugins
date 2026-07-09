## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new database schema after the migration replaces the `advisory_status` lookup table with an enum column. Define an `AdvisoryStatusEnum` Rust enum mapped to the PostgreSQL `advisory_status_enum` type, update the `advisory` entity to use the new `status` enum field instead of `status_id`, and remove the `advisory_status` entity entirely.

## Files to Modify
- `entity/src/advisory.rs` -- replace `status_id: i32` FK field with `status: AdvisoryStatusEnum` enum field; remove the `Relation` variant referencing `advisory_status`
- `entity/src/lib.rs` -- remove `pub mod advisory_status;` module declaration and any re-exports of the advisory_status entity

## Implementation Notes
- Define a Rust enum `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected`. Derive `DeriveActiveEnum` from SeaORM for automatic mapping to the PostgreSQL `advisory_status_enum` type. Use `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]` and annotate each variant with `#[sea_orm(string_value = "New")]` etc.
- In `entity/src/advisory.rs`, replace the `status_id` column definition with a `status` column using the new enum type.
- Remove any `Relation` variant in the advisory entity's `RelationDef` that references `AdvisoryStatus` or the `advisory_status` table.
- Delete `entity/src/advisory_status.rs` entirely -- this entity file is no longer needed after the lookup table is dropped.
- Remove the `advisory_status` module declaration from `entity/src/lib.rs`.
- Per CONVENTIONS.md §Framework: use SeaORM `DeriveActiveEnum` for mapping Rust enums to PostgreSQL enum types.
  Applies: task modifies `entity/src/advisory.rs` matching the convention's SeaORM entity file scope.
- Reference `entity/src/sbom.rs` for the established SeaORM entity pattern (column definitions, relations, derives).

## Reuse Candidates
- `entity/src/advisory.rs` -- existing advisory entity showing the current SeaORM entity structure, column definitions, and relation patterns
- `entity/src/sbom.rs` -- sibling entity demonstrating the standard SeaORM entity pattern to follow

## Acceptance Criteria
- [ ] `AdvisoryStatusEnum` enum is defined with variants New, Analyzing, Fixed, Rejected and derives `DeriveActiveEnum`
- [ ] `entity/src/advisory.rs` uses `status: AdvisoryStatusEnum` column instead of `status_id: i32`
- [ ] Relation to `advisory_status` is removed from the advisory entity
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer declares or re-exports the `advisory_status` module
- [ ] `cargo build -p entity` compiles without errors

## Test Requirements
- [ ] Verify entity crate compiles against the migrated database schema
- [ ] Verify `AdvisoryStatusEnum` serialization round-trips correctly (Rust enum to PostgreSQL enum and back)
- [ ] Verify no remaining references to `advisory_status` entity in the entity crate

## Verification Commands
- `cargo build -p entity` -- entity crate compiles successfully
- `cargo test -p entity` -- entity tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 2 -- Create database migration for advisory status enum
