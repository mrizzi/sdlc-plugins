# Task 3 -- Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new database schema. Replace the `status_id` foreign key field in the `advisory` entity with a `status` field mapped to the `advisory_status_enum` PostgreSQL enum type. Remove the `advisory_status` entity file entirely since the lookup table no longer exists. Update the entity module's `lib.rs` to remove the `advisory_status` module registration.

## Files to Modify
- `entity/src/advisory.rs` -- replace `status_id: i32` foreign key field with `status: AdvisoryStatusEnum` enum field; remove the `Relation` to `advisory_status`; add SeaORM `DeriveActiveEnum` mapping for the enum type
- `entity/src/lib.rs` -- remove `pub mod advisory_status;` module declaration and re-export

## Files to Create
- None (the `advisory_status.rs` file is being removed, not created)

## Implementation Notes
- Define a Rust enum `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected` in `entity/src/advisory.rs` (or a shared location). Use SeaORM's `DeriveActiveEnum` derive macro to map it to the PostgreSQL `advisory_status_enum` type:
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
- Follow the existing entity patterns in `entity/src/sbom.rs` for struct layout, derives, and relation definitions.
- Remove the `Relation::AdvisoryStatus` variant from the advisory entity's `Relation` enum and its `RelationDef` implementation.
- Remove the `Related<advisory_status::Entity>` impl block from the advisory entity.
- The `advisory_status.rs` entity file should be deleted entirely -- it corresponds to the dropped `advisory_status` table.
- Update `entity/src/lib.rs` to remove the `advisory_status` module and any re-exports.

## Reuse Candidates
- `entity/src/sbom.rs` -- reference for SeaORM entity structure, derives, and relation patterns
- `entity/src/package.rs` -- reference for entity field type patterns

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` has a `status` field of type `AdvisoryStatusEnum` instead of `status_id`
- [ ] `AdvisoryStatusEnum` is defined with `DeriveActiveEnum` mapping to `advisory_status_enum` PostgreSQL type
- [ ] All relations and references to `advisory_status` entity are removed from `advisory.rs`
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer declares or exports the `advisory_status` module
- [ ] The entity crate compiles without errors (`cargo check -p entity`)

## Test Requirements
- [ ] `cargo check -p entity` compiles successfully with no errors
- [ ] No remaining references to `advisory_status` entity in the entity crate (verified via grep)

## Verification Commands
- `cargo check -p entity` -- entity crate compiles without errors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 2 -- Create atomic migration to replace advisory_status table with enum column
