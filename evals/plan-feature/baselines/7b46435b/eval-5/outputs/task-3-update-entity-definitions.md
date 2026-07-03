## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update SeaORM entity definitions to reflect the new database schema after the advisory_status_enum migration. The advisory entity must use a Rust enum mapped to the PostgreSQL advisory_status_enum type via SeaORM's DeriveActiveEnum. The advisory_status entity module must be removed since the lookup table no longer exists.

## Files to Modify
- `entity/src/advisory.rs` — replace status_id integer FK column with a status enum column using DeriveActiveEnum mapping to advisory_status_enum
- `entity/src/lib.rs` — remove the advisory_status module declaration and re-export

## Implementation Notes
- Define an `AdvisoryStatus` enum with variants `New`, `Analyzing`, `Fixed`, `Rejected` and derive `DeriveActiveEnum` with `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]`
- Each variant needs a `#[sea_orm(string_value = "...")]` attribute matching the PostgreSQL enum value
- Remove the `advisory_status` module from `entity/src/lib.rs` — the file `entity/src/advisory_status.rs` is no longer needed since the lookup table has been dropped
- Remove any `Relation` to `advisory_status` from the advisory entity's `RelationDef` impl
- Follow the existing entity pattern in `entity/src/sbom.rs` for entity structure

## Reuse Candidates
- `entity/src/sbom.rs` — existing SeaORM entity demonstrating the entity definition pattern used in this project

## Acceptance Criteria
- [ ] advisory entity has a status field of type AdvisoryStatus enum
- [ ] AdvisoryStatus enum is mapped to PostgreSQL advisory_status_enum via DeriveActiveEnum
- [ ] advisory_status entity module is removed from lib.rs
- [ ] No remaining references to advisory_status entity or status_id column in the entity crate
- [ ] Entity crate compiles without errors

## Test Requirements
- [ ] Entity crate compiles: cargo build -p entity
- [ ] AdvisoryStatus enum correctly maps all four values: New, Analyzing, Fixed, Rejected

## Verification Commands
- `cargo build -p entity` — entity crate compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005
- Depends on: Task 2 — Database migration (schema must exist before entities reflect it)
