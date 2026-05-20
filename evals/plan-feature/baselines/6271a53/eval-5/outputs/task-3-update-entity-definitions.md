## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema. Replace the `status_id` foreign key field in the `advisory` entity with a `status` field of the new `advisory_status_enum` enum type. Remove the `advisory_status` entity file entirely and update `lib.rs` to remove its module registration and any re-exports.

## Files to Modify
- `entity/src/advisory.rs` -- Replace `status_id: i32` foreign key field with `status: AdvisoryStatusEnum` enum field; remove the relation to `advisory_status`; add SeaORM enum derive for `AdvisoryStatusEnum`
- `entity/src/lib.rs` -- Remove `mod advisory_status` and any re-exports of the advisory_status entity

## Files to Create
None -- the `advisory_status.rs` file is being removed, not created.

## Implementation Notes
- Define a Rust enum `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected` that derives `sea_orm::EnumIter` and `sea_orm::DeriveActiveEnum` to map to the PostgreSQL `advisory_status_enum` type
- The enum should be defined in `entity/src/advisory.rs` alongside the `Model` struct, or in a separate submodule if the project convention separates enums
- Remove the `Relation::AdvisoryStatus` variant from the advisory entity's `Relation` enum and its `RelationTrait` implementation
- Remove the `Related<advisory_status::Entity>` implementation from the advisory entity
- Follow the existing entity patterns in `entity/src/sbom.rs` for struct layout and derive macros
- The `advisory_status.rs` file should be deleted entirely -- it will no longer be needed

## Reuse Candidates
- `entity/src/sbom.rs` -- Reference for entity struct layout, derive macros, and relation patterns
- `entity/src/advisory.rs` -- Current advisory entity showing the existing pattern to modify

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` has a `status` field of type `AdvisoryStatusEnum` instead of `status_id: i32`
- [ ] `AdvisoryStatusEnum` enum is defined with variants New, Analyzing, Fixed, Rejected and proper SeaORM derives
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer references `advisory_status`
- [ ] All relation definitions to `advisory_status` are removed from the advisory entity
- [ ] `cargo check -p entity` compiles without errors

## Test Requirements
- [ ] Verify `cargo check -p entity` passes with the updated entity definitions
- [ ] Verify the `AdvisoryStatusEnum` correctly maps to PostgreSQL enum values

## Verification Commands
- `cargo check -p entity` -- entity crate compiles successfully

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 2 -- Create migration for advisory_status_enum and drop lookup table
