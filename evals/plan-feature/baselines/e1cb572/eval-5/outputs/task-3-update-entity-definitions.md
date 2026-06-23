# Task 3 — Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity layer to reflect the new schema after the migration. Replace the `status_id` foreign key field in the advisory entity with a `status` field of the new enum type, define the `AdvisoryStatusEnum` Rust enum with SeaORM's `DeriveActiveEnum` derive macro, and remove the `advisory_status` entity since the lookup table has been dropped.

## Files to Modify
- `entity/src/advisory.rs` -- replace `status_id: i32` column with `status: AdvisoryStatusEnum` column; add the `AdvisoryStatusEnum` enum definition with `DeriveActiveEnum` derive macro; remove the `Relation` to `advisory_status`
- `entity/src/lib.rs` -- remove the `pub mod advisory_status;` declaration and re-export

## Files to Create
- None -- the `AdvisoryStatusEnum` definition belongs directly in `entity/src/advisory.rs` alongside the entity, following SeaORM conventions for co-located enum definitions

## Implementation Notes
Define the enum using SeaORM's active enum pattern in `entity/src/advisory.rs`:

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

In the advisory entity `Model` struct, replace `pub status_id: i32` with `pub status: AdvisoryStatusEnum`.

In the `Column` enum, replace `StatusId` with `Status`.

In the `Relation` enum, remove the variant that linked to `advisory_status::Entity`.

Delete `entity/src/advisory_status.rs` entirely -- this entity is no longer needed since the lookup table has been dropped. Remove the corresponding `pub mod advisory_status;` from `entity/src/lib.rs`.

Follow the existing entity patterns in `entity/src/sbom.rs` for struct layout and derive macros. Check `entity/src/sbom_advisory.rs` for any references to `advisory_status` and update if needed.

Per CONVENTIONS.md §Framework: Axum for HTTP, SeaORM for database. Applies: task modifies `entity/src/advisory.rs` matching the convention's SeaORM entity scope.

## Reuse Candidates
- `entity/src/sbom.rs` -- reference entity pattern for Model struct, Column enum, Relation enum, and derive macros
- `entity/src/advisory.rs` -- existing advisory entity to modify in-place

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with variants New, Analyzing, Fixed, Rejected
- [ ] The advisory `Model` struct uses `status: AdvisoryStatusEnum` instead of `status_id: i32`
- [ ] The advisory `Relation` enum no longer references `advisory_status`
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer exports `advisory_status`
- [ ] The entity crate compiles without errors

## Test Requirements
- [ ] `cargo check -p entity` compiles successfully
- [ ] Verify that no remaining references to `advisory_status` entity exist in the entity crate
- [ ] SeaORM enum mapping correctly maps `AdvisoryStatusEnum` variants to PostgreSQL `advisory_status_enum` values

## Verification Commands
- `cargo check -p entity` -- entity crate compiles without errors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 2 -- Add database migration for advisory status enum

`[sdlc-workflow] Description digest: sha256-md:c4a8b2d6e0f3a7c1d5e9f2b4a6c8d0e3f5a7b9c1d3e5f7a9b1c3d5e7f9a0b2c4`
