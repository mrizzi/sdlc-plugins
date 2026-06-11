# Task 3 — Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new database schema after the advisory status enum migration. The `advisory` entity must replace the `status_id` foreign key integer field with a `status` field of the new `AdvisoryStatusEnum` type. The `advisory_status` entity file must be removed since the lookup table no longer exists. All entity re-exports in `lib.rs` must be updated accordingly.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` foreign key field with `status: AdvisoryStatusEnum` enum field; remove the `Relation` to `advisory_status`; define the `AdvisoryStatusEnum` Rust enum with SeaORM `DeriveActiveEnum` derive macro
- `entity/src/lib.rs` — remove the `pub mod advisory_status` re-export

## Files to Create
- None (advisory_status.rs is being removed, not created)

## Implementation Notes
- Define a Rust enum `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected` in `entity/src/advisory.rs`, using SeaORM's `DeriveActiveEnum` derive macro to map it to the PostgreSQL `advisory_status_enum` type.
- Follow the existing entity pattern in `entity/src/sbom.rs` for struct definition and derive macros.
- Remove the `Relation::AdvisoryStatus` variant from the `advisory` entity's `RelationDef` implementation since the foreign key relationship no longer exists.
- The `advisory_status.rs` entity file should be deleted entirely — it maps to a table that no longer exists after the migration.
- Update `entity/src/lib.rs` to remove the `pub mod advisory_status` line.
- Per docs/constraints.md section 5 (Code Change Rules): inspect existing entity files before modifying to ensure correct pattern adherence.

## Reuse Candidates
- `entity/src/sbom.rs` — reference entity pattern showing SeaORM entity struct definition, column enum, and relation definitions
- `entity/src/package.rs` — another entity example for consistent struct and derive patterns

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with `DeriveActiveEnum` mapping to `advisory_status_enum` PostgreSQL type
- [ ] `entity/src/advisory.rs` model uses `status: AdvisoryStatusEnum` instead of `status_id: i32`
- [ ] `Relation::AdvisoryStatus` is removed from advisory entity relations
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer exports `advisory_status` module
- [ ] Entity crate compiles without errors

## Test Requirements
- [ ] `cargo check -p entity` compiles successfully
- [ ] Any existing entity unit tests pass after modifications

## Verification Commands
- `cargo check -p entity` — entity crate compiles
- `cargo test -p entity` — entity tests pass (if any)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create database migration for advisory status enum

[sdlc-workflow] Description digest: sha256-md:5994ebf369b9960ae5d405a926afe57b3463dd2fc7450b52794447343557d0c1
