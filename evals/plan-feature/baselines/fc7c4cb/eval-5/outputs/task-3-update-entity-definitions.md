# Task 3 — Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity layer to reflect the new database schema. Modify `entity/src/advisory.rs` to replace the `status_id` foreign key field with a `status` field using the `advisory_status_enum` PostgreSQL enum type. Remove `entity/src/advisory_status.rs` since the lookup table no longer exists. Update `entity/src/lib.rs` to remove the `advisory_status` module declaration and re-export.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` FK field with `status: AdvisoryStatusEnum` enum field; remove the `Relation` to `advisory_status`; add SeaORM `DeriveActiveEnum` mapping for the new enum type
- `entity/src/lib.rs` — remove `pub mod advisory_status` declaration/re-export

## Files to Delete
- `entity/src/advisory_status.rs` — lookup table entity no longer needed

## Implementation Notes
- In `entity/src/advisory.rs`, define a Rust enum `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected` and derive `DeriveActiveEnum` from SeaORM to map it to the PostgreSQL `advisory_status_enum` type.
- Remove the `Relation::AdvisoryStatus` variant from the `Relation` enum in `advisory.rs` and its corresponding `RelationTrait` implementation.
- Follow the existing entity pattern in `entity/src/sbom.rs` for struct field definitions and derive macros.
- Update `Cargo.toml` if any dependencies need adjustment for enum support (SeaORM's `derive` feature should already be enabled).

## Reuse Candidates
- `entity/src/sbom.rs` — reference for SeaORM entity struct pattern, derive macros, and relation definitions
- `entity/src/package.rs` — reference for entity field definitions and column enum mapping

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with `DeriveActiveEnum` mapping to `advisory_status_enum`
- [ ] `entity/src/advisory.rs` Model struct has `status: AdvisoryStatusEnum` field instead of `status_id: i32`
- [ ] `entity/src/advisory.rs` no longer contains a `Relation` to `advisory_status`
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer declares or re-exports `advisory_status`
- [ ] `cargo check -p entity` compiles without errors

## Test Requirements
- [ ] Verify `cargo check -p entity` passes with no compilation errors
- [ ] Verify that the `AdvisoryStatusEnum` correctly maps all four values: New, Analyzing, Fixed, Rejected

## Verification Commands
- `cargo check -p entity` — compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create database migration for advisory status enum

[sdlc-workflow] Description digest: sha256:11209911e93dff06097d62e3d37c5cb9d1564cd92923853a6cd95a9444dfb569
