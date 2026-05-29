# Task 3 -- Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity layer to reflect the new database schema after the enum migration. Replace the `status_id` foreign key field in the advisory entity with a `status` field of type `advisory_status_enum`. Remove the `advisory_status` entity file since the lookup table no longer exists. Define a Rust enum that maps to the PostgreSQL `advisory_status_enum` type using SeaORM's `DeriveActiveEnum` derive macro.

## Files to Modify
- `entity/src/advisory.rs` -- replace `status_id: i32` foreign key field with `status: AdvisoryStatusEnum` enum field; remove the `Relation` to `advisory_status` table; update any `Related` trait implementations that reference the advisory_status entity
- `entity/src/lib.rs` -- remove the `pub mod advisory_status;` module declaration

## Files to Create
- `entity/src/advisory_status_enum.rs` -- define the `AdvisoryStatusEnum` Rust enum with `DeriveActiveEnum` mapping to the PostgreSQL enum type, with variants: New, Analyzing, Fixed, Rejected

## Implementation Notes
- Use SeaORM's `DeriveActiveEnum` derive macro to map the Rust enum to the PostgreSQL `advisory_status_enum` type. Example pattern:
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
- Follow the existing entity patterns in `entity/src/sbom.rs` and `entity/src/package.rs` for struct layout, derives, and attribute macros
- In `entity/src/advisory.rs`, the `Column::StatusId` variant must be replaced with `Column::Status` and its column type must be updated to reference the enum
- Remove the `Relation::AdvisoryStatus` variant and any `impl Related<advisory_status::Entity>` block
- The file `entity/src/advisory_status.rs` should be deleted (not just emptied) since the lookup table is dropped
- Per docs/constraints.md SS2 (Commit Rules): commit message must follow Conventional Commits format and reference TC-9005

## Reuse Candidates
- `entity/src/sbom.rs` -- reference for SeaORM entity struct layout, derives, and Column/Relation definitions
- `entity/src/package.rs` -- reference for entity struct patterns in this codebase

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` has a `status` field of type `AdvisoryStatusEnum` instead of `status_id: i32`
- [ ] `entity/src/advisory_status_enum.rs` defines the enum with all four variants (New, Analyzing, Fixed, Rejected)
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer declares the `advisory_status` module and exports the new `advisory_status_enum` module
- [ ] The advisory entity has no `Relation` or `Related` impl referencing the `advisory_status` table
- [ ] `cargo build -p entity` compiles without errors

## Test Requirements
- [ ] Verify `cargo build -p entity` succeeds with the updated entity definitions
- [ ] Verify that the `AdvisoryStatusEnum` correctly derives `DeriveActiveEnum` and maps to all four PostgreSQL enum values

## Verification Commands
- `cargo build -p entity` -- compiles without errors
- `cargo test -p entity` -- all entity tests pass (if any exist)

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 2 -- Create database migration for advisory_status_enum

[sdlc-workflow] Description digest: sha256:c6e572811f581b2e254012ab68ca402d5e4bd00791afbf6bcfad950658812768
