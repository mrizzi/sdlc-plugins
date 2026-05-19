# Task 3 — Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new database schema after the migration replaces the `advisory_status` lookup table with an enum column. Modify the `advisory` entity to use the new `status` enum column, remove the `advisory_status` entity module, and update the entity library exports.

## Files to Modify
- `entity/src/advisory.rs` — Replace the `status_id` integer/FK column definition with a `status` column using the `AdvisoryStatusEnum` type; remove the `Relation` to `advisory_status`; add a SeaORM enum mapping for `advisory_status_enum`
- `entity/src/lib.rs` — Remove the `pub mod advisory_status;` export and any re-exports of `AdvisoryStatus` entity types

## Implementation Notes
- Define a Rust enum `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected` and derive `sea_orm::EnumIter`, `sea_orm::DeriveActiveEnum` with `db_type = "Enum"` and `enum_name = "advisory_status_enum"`
- In the `advisory` entity's `Column` enum, replace `StatusId` with `Status` and map it to the new `AdvisoryStatusEnum` type
- Remove the `Relation::AdvisoryStatus` variant and its `RelationDef` implementation from the advisory entity's `Relation` enum
- Delete `entity/src/advisory_status.rs` as this entity is no longer needed
- Follow the existing entity patterns in `entity/src/sbom.rs` and `entity/src/package.rs` for structure and derives
- Per docs/constraints.md: inspect existing entity code before modifying; follow patterns in Implementation Notes
- Per docs/constraints.md: commits must reference Jira issue ID, follow Conventional Commits, and include AI attribution trailer
- Per docs/constraints.md: PR must specify `--base TC-9005`

## Reuse Candidates
- `entity/src/advisory.rs` — Existing advisory entity with Column, Relation, and Model definitions to be modified in place
- `entity/src/sbom.rs` — Reference for SeaORM entity structure and derive patterns

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with variants New, Analyzing, Fixed, Rejected
- [ ] `entity/src/advisory.rs` Column enum uses `Status` instead of `StatusId` with the correct enum type
- [ ] `entity/src/advisory.rs` Relation enum no longer includes `AdvisoryStatus`
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer exports `advisory_status` module
- [ ] Entity crate compiles without errors

## Test Requirements
- [ ] Verify the entity crate compiles (`cargo check -p entity`)
- [ ] Verify the `AdvisoryStatusEnum` derives are correct and the enum maps to `advisory_status_enum` in PostgreSQL

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
