# Task 3 -- Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity layer to reflect the new database schema. The `advisory` entity must replace its `status_id` integer foreign key with a `status` field of the new `AdvisoryStatusEnum` enum type. The `advisory_status` entity file must be removed since the lookup table no longer exists. The entity `lib.rs` must be updated to remove the `advisory_status` module.

## Files to Modify
- `entity/src/advisory.rs` -- Replace `status_id: i32` column with `status: AdvisoryStatusEnum`; define `AdvisoryStatusEnum` as a SeaORM-compatible enum with variants `New`, `Analyzing`, `Fixed`, `Rejected`; remove the `Relation` to `advisory_status` if one exists
- `entity/src/lib.rs` -- Remove `pub mod advisory_status;` re-export and any related use statements

## Files to Create
- None (the `advisory_status.rs` file is deleted, not created)

## Implementation Notes
- In `entity/src/advisory.rs`, define the enum using SeaORM's `DeriveActiveEnum` derive macro:
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
- Update the `Model` struct in `entity/src/advisory.rs` to replace `pub status_id: i32` with `pub status: AdvisoryStatusEnum`.
- Update the `Column` enum to replace `StatusId` with `Status`.
- Remove any `RelationDef` pointing to `advisory_status::Entity` from the `Relation` enum.
- In `entity/src/lib.rs`, remove the `pub mod advisory_status;` line. Verify no other entity files import from `advisory_status`.
- Delete `entity/src/advisory_status.rs` entirely.
- Follow the pattern used by other entity files (e.g., `entity/src/sbom.rs`) for struct and derive macro conventions.

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with four variants matching the database enum values
- [ ] `advisory::Model` has a `status: AdvisoryStatusEnum` field instead of `status_id: i32`
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer references `advisory_status`
- [ ] Entity crate compiles without errors (`cargo build -p entity`)

## Test Requirements
- [ ] `cargo build -p entity` compiles successfully
- [ ] Verify that `AdvisoryStatusEnum` serializes/deserializes correctly to the four expected string values
- [ ] No compilation errors in downstream crates that depend on `entity`

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 2 -- Create database migration for advisory status enum
