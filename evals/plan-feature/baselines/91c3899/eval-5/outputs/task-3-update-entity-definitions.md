# Task 3 — Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new database schema after the enum migration. The `advisory` entity must use the new `advisory_status_enum` column instead of the `status_id` foreign key, and the `advisory_status` entity must be removed entirely since the lookup table no longer exists.

## Files to Modify
- `entity/src/advisory.rs` — Replace `status_id` integer/FK column with `status` enum column using SeaORM's `DeriveActiveEnum` mapping; remove the relation to `advisory_status`
- `entity/src/lib.rs` — Remove the `advisory_status` module re-export

## Files to Create
- None (the `advisory_status.rs` entity file is deleted, not created)

## Implementation Notes
- Define a Rust enum `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected` and derive `DeriveActiveEnum` from SeaORM to map it to the PostgreSQL `advisory_status_enum` type
- The enum definition can live in `entity/src/advisory.rs` alongside the entity, or in a shared types module if one exists
- Update the `Model` struct in `advisory.rs` to replace `status_id: i32` with `status: AdvisoryStatusEnum`
- Remove the `Relation::AdvisoryStatus` variant and its `RelationDef` implementation from the advisory entity
- Remove or update any `Related<advisory_status::Entity>` impl on the advisory entity
- Check `entity/src/sbom_advisory.rs` — if it references `advisory_status`, update or verify it does not depend on the dropped table
- Per docs/constraints.md §5.2: inspect existing entity code before modifying
- Per docs/constraints.md §2 (Commit Rules): commit must reference TC-9005 in the footer and follow Conventional Commits format

## Reuse Candidates
- `entity/src/advisory.rs` — Current advisory entity showing the existing `status_id` column and relation definitions to be replaced
- `entity/src/sbom.rs` — Sibling entity demonstrating SeaORM entity patterns, column definitions, and relation setup in this project

## Acceptance Criteria
- [ ] `advisory.rs` entity uses `AdvisoryStatusEnum` for the `status` column
- [ ] `AdvisoryStatusEnum` derives `DeriveActiveEnum` and maps to PostgreSQL `advisory_status_enum`
- [ ] `advisory_status.rs` entity file is removed
- [ ] `lib.rs` no longer exports `advisory_status` module
- [ ] No remaining references to `advisory_status` entity in the `entity/` crate
- [ ] Project compiles without errors after changes (`cargo check -p entity`)

## Test Requirements
- [ ] `cargo check -p entity` compiles without errors
- [ ] Enum variants map correctly to database values (verified by integration tests in Task 6)

## Verification Commands
- `cargo check -p entity` — entity crate compiles cleanly

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create database migration for advisory status enum
