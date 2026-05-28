## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema: replace the `status_id` foreign key field in the advisory entity with a `status` enum field, and remove the `advisory_status` entity entirely. This task bridges the database migration and the service/endpoint changes by ensuring the ORM layer correctly maps the new enum column.

## Files to Modify
- `entity/src/advisory.rs` — Replace the `status_id: i32` field (and its relation to `advisory_status`) with a `status: AdvisoryStatusEnum` field mapped to the `advisory_status_enum` PostgreSQL type
- `entity/src/lib.rs` — Remove the `advisory_status` module registration and re-export

## Files to Create
None — no new entity files needed.

## Implementation Notes
- SeaORM supports PostgreSQL enums via the `DeriveActiveEnum` derive macro. Define an `AdvisoryStatusEnum` Rust enum with variants `New`, `Analyzing`, `Fixed`, `Rejected` and derive `DeriveActiveEnum` with the `db_type` set to the PostgreSQL enum name `advisory_status_enum`.
- In `entity/src/advisory.rs`, replace the `status_id` column definition with a `status` column of type `AdvisoryStatusEnum`. Remove any `RelationDef` or `Related<advisory_status::Entity>` impl that references the old lookup table.
- Remove `entity/src/advisory_status.rs` entirely (delete the file).
- Update `entity/src/lib.rs` to remove the `pub mod advisory_status;` line and any re-exports of advisory_status types.
- Follow the existing entity patterns in `entity/src/sbom.rs` and `entity/src/package.rs` for struct layout and derive macro usage.

## Reuse Candidates
- `entity/src/sbom.rs` — Demonstrates the entity definition pattern (Model struct, Relation enum, ActiveModel) used throughout the project
- `entity/src/package.rs` — Another entity example showing column definitions and relation patterns

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` contains a `status` field of type `AdvisoryStatusEnum` instead of `status_id`
- [ ] `AdvisoryStatusEnum` is defined with variants New, Analyzing, Fixed, Rejected and uses `DeriveActiveEnum`
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer references `advisory_status`
- [ ] The entity crate compiles without errors

## Test Requirements
- [ ] Entity crate compiles successfully (`cargo check -p entity`)
- [ ] Verify the `AdvisoryStatusEnum` enum serializes/deserializes correctly for all four variants

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create advisory_status_enum migration
