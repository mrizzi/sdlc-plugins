# Task 3 -- Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity layer to reflect the new database schema after the migration. Replace the `status_id` foreign key field in the advisory entity with a `status` enum field, define the `AdvisoryStatusEnum` Rust enum with SeaORM derive macros, and remove the `advisory_status` entity file that represented the now-dropped lookup table.

## Files to Modify
- `entity/src/advisory.rs` -- replace `status_id: i32` column with `status: AdvisoryStatusEnum` column; add the `AdvisoryStatusEnum` enum definition with `DeriveActiveEnum` derive macro; remove the `Relation` to `advisory_status`
- `entity/src/lib.rs` -- remove the `pub mod advisory_status;` re-export

## Implementation Notes
- Define the `AdvisoryStatusEnum` enum in `entity/src/advisory.rs` using SeaORM's `DeriveActiveEnum` macro:
  ```rust
  #[derive(Debug, Clone, PartialEq, Eq, EnumIter, DeriveActiveEnum)]
  #[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]
  pub enum AdvisoryStatusEnum {
      #[sea_orm(string_value = "New")]
      New,
      #[sea_orm(string_value = "Analyzing")]
      Analyzing,
      #[sea_orm(string_value = "Fixed")]
      Fixed,
      #[sea_orm(string_value = "Rejected")]
      Rejected,
  }
  ```
- In the `Model` struct, replace `pub status_id: i32` with `pub status: AdvisoryStatusEnum`.
- In the `Relation` enum, remove the variant that linked to `advisory_status::Entity`.
- In the `Column` enum, replace `StatusId` with `Status`.
- Follow the existing entity pattern in `entity/src/sbom.rs` for struct layout and derive macros.
- Delete `entity/src/advisory_status.rs` entirely -- this entity is no longer needed since the lookup table has been dropped.
- Check `entity/src/sbom_advisory.rs` for any references to `advisory_status` and update if needed.

Per CONVENTIONS.md &sect;Framework: SeaORM for database -- use SeaORM derive macros (`DeriveEntityModel`, `DeriveActiveEnum`) for entity definitions.
Applies: task modifies `entity/src/advisory.rs` matching the convention's entity module scope.

## Reuse Candidates
- `entity/src/sbom.rs` -- reference entity pattern for Model struct, Column enum, Relation enum, and derive macros
- `entity/src/advisory.rs` -- existing advisory entity to modify in-place

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` contains an `AdvisoryStatusEnum` enum with variants New, Analyzing, Fixed, Rejected
- [ ] The advisory `Model` struct uses `status: AdvisoryStatusEnum` instead of `status_id: i32`
- [ ] The advisory `Relation` enum no longer references `advisory_status`
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer exports `advisory_status`
- [ ] The entity crate compiles without errors

## Test Requirements
- [ ] `cargo check -p entity` compiles successfully
- [ ] Verify that no remaining references to `advisory_status` entity exist in the entity crate

## Verification Commands
- `cargo check -p entity` -- entity crate compiles without errors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 2 -- Create migration: add advisory_status_enum type, backfill status column, drop lookup table
