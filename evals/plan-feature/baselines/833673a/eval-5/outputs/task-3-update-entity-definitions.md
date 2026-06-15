## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema after the advisory status migration. Modify the `advisory` entity to replace the `status_id` foreign key field with a `status` field of type `advisory_status_enum`. Remove the `advisory_status` entity file since the lookup table no longer exists. Update `entity/src/lib.rs` to remove the `advisory_status` module export.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` foreign key field with `status: AdvisoryStatusEnum` enum field; remove the relation to `advisory_status`; add the `AdvisoryStatusEnum` enum definition with SeaORM derive macros
- `entity/src/lib.rs` — remove the `pub mod advisory_status` module declaration

## Files to Create
(none — the advisory_status entity file is being removed, not created)

## Implementation Notes
Define the `AdvisoryStatusEnum` enum in `entity/src/advisory.rs` using SeaORM's `DeriveActiveEnum` macro with `db_type = "Enum"` and `enum_name = "advisory_status_enum"`. The enum variants should be `New`, `Analyzing`, `Fixed`, `Rejected` matching the PostgreSQL enum values.

Follow the existing entity pattern in `entity/src/sbom.rs` for struct definition style and derive macros.

Remove any `Relation` variant that pointed to `AdvisoryStatus` in the advisory entity's `RelationDef` implementation.

Update the `entity/Cargo.toml` if the `advisory_status.rs` file removal requires changes to module declarations (though typically SeaORM entities are registered in `lib.rs`).

## Reuse Candidates
- `entity/src/sbom.rs` — existing SeaORM entity definition demonstrating the derive macro pattern and column attribute style to follow

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` has an `AdvisoryStatusEnum` enum with variants New, Analyzing, Fixed, Rejected
- [ ] `entity/src/advisory.rs` uses the `status` field with type `AdvisoryStatusEnum` instead of `status_id`
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer exports the `advisory_status` module
- [ ] The entity crate compiles without errors (`cargo check -p entity`)

## Test Requirements
- [ ] `cargo check -p entity` passes with no errors
- [ ] The `AdvisoryStatusEnum` enum serializes and deserializes correctly with SeaORM

## Verification Commands
- `cargo check -p entity` — entity crate compiles cleanly

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256-md:2258a1208fec32b432877efce0fadc4556e40e6f756e185cd7f9e7cef994742a
