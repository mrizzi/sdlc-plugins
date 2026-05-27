## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new advisory status enum schema. Replace the `status_id` foreign key field in `entity/src/advisory.rs` with a `status` field of the new `advisory_status_enum` type using SeaORM's enum mapping. Remove the `advisory_status.rs` entity file since the lookup table no longer exists, and remove its re-export from `entity/src/lib.rs`.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` foreign key field with `status: AdvisoryStatusEnum` enum field; remove the `Relation` to `advisory_status` table; update the `ActiveModel` and any `impl` blocks that reference `status_id`
- `entity/src/lib.rs` — remove the `pub mod advisory_status;` re-export

## Files to Create
- (none — the enum type definition should be added within `entity/src/advisory.rs` or a shared types module)

## Implementation Notes
- Define the `AdvisoryStatusEnum` Rust enum with `#[derive(EnumIter, DeriveActiveEnum)]` and map it to the PostgreSQL `advisory_status_enum` type. Follow SeaORM's `DeriveActiveEnum` pattern for mapping enum variants to database values.
- The enum variants should be: `New`, `Analyzing`, `Fixed`, `Rejected` — matching the PostgreSQL enum values exactly.
- Remove the `Relation::AdvisoryStatus` variant from the `Relation` enum in the advisory entity, and remove the corresponding `impl Related<advisory_status::Entity>` block.
- Look at how other entities in `entity/src/` define their fields and relations (e.g., `sbom.rs`, `package.rs`) to follow the established pattern.
- The `advisory_status.rs` file should be deleted entirely (not left empty).

## Reuse Candidates
- `entity/src/sbom.rs` — reference for entity field definitions and relation patterns in this project
- `entity/src/package.rs` — reference for entity structure conventions

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` has a `status: AdvisoryStatusEnum` field instead of `status_id: i32`
- [ ] `AdvisoryStatusEnum` is defined with variants New, Analyzing, Fixed, Rejected using `DeriveActiveEnum`
- [ ] The `Relation` to `advisory_status` table is removed
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer re-exports `advisory_status`
- [ ] `cargo check -p entity` compiles without errors

## Test Requirements
- [ ] Verify the entity compiles with `cargo check -p entity`
- [ ] Verify the `AdvisoryStatusEnum` correctly maps all four variants to their PostgreSQL enum values

## Verification Commands
- `cargo check -p entity` — compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create migration for advisory_status_enum
