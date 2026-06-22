# Task 3 — Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema where `advisory.status` is a PostgreSQL enum column instead of a foreign key to the `advisory_status` lookup table. This involves modifying the `advisory` entity to use an enum field and removing the `advisory_status` entity if it exists.

## Files to Modify
- `entity/src/advisory.rs` — replace the `status_id` integer foreign key field with a `status` field of type `AdvisoryStatusEnum`; remove the `Relation` to `advisory_status`; add the `AdvisoryStatusEnum` derive enum mapping SeaORM to the PostgreSQL `advisory_status_enum` type
- `entity/src/lib.rs` — remove the `advisory_status` module re-export if present; ensure `AdvisoryStatusEnum` is exported

## Files to Create
- None expected, but verify during implementation whether `entity/src/advisory_status.rs` exists. If it does, it should be deleted (the lookup table entity is no longer needed).

## Implementation Notes
- Follow the SeaORM enum mapping pattern: define an enum with `#[derive(Debug, Clone, PartialEq, Eq, EnumIter, DeriveActiveEnum)]` and `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]` with value attributes mapping each variant to its database string.
- The enum variants should be: `New`, `Analyzing`, `Fixed`, `Rejected` — matching the PostgreSQL enum values.
- In the `Model` struct, replace `pub status_id: i32` with `pub status: AdvisoryStatusEnum`.
- Remove the `Relation::AdvisoryStatus` variant from the `Relation` enum and its corresponding `RelationTrait` implementation.
- Remove any `impl Related<super::advisory_status::Entity> for Entity` block.
- Reference the existing entity patterns in `entity/src/sbom.rs` and `entity/src/package.rs` for the struct and relation conventions.
- Per docs/constraints.md §5.2: inspect `entity/src/advisory.rs` before modifying to understand the current field definitions and relation setup.

## Reuse Candidates
- `entity/src/sbom.rs` — reference for SeaORM entity struct patterns, relation definitions, and derive macros used in this project
- `entity/src/package.rs` — reference for field types and entity conventions

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with variants New, Analyzing, Fixed, Rejected
- [ ] The `Model` struct uses `status: AdvisoryStatusEnum` instead of `status_id: i32`
- [ ] The `Relation` enum no longer references `advisory_status`
- [ ] The `advisory_status` entity module is removed (if it existed)
- [ ] The entity crate compiles without errors (`cargo check -p entity`)

## Test Requirements
- [ ] Verify the entity crate compiles: `cargo check -p entity`
- [ ] Verify that `AdvisoryStatusEnum` can be serialized/deserialized correctly by SeaORM (covered by integration tests in Task 6)

## Verification Commands
- `cargo check -p entity` — compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create migration to replace advisory_status table with enum column
