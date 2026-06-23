# Task 3 — Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema where `advisory.status` is an enum column instead of a foreign key to the `advisory_status` lookup table. This involves modifying the `advisory` entity to replace the `status_id` integer column with a `status` enum column mapped to the `advisory_status_enum` PostgreSQL type, and removing any entity module for the now-dropped `advisory_status` table.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id` foreign key column definition with `status` enum column using SeaORM's `DeriveActiveEnum` mapping to `advisory_status_enum`
- `entity/src/lib.rs` — remove `advisory_status` module registration if present; ensure `advisory` module is still registered

## Implementation Notes
- Define a Rust enum (e.g., `AdvisoryStatusEnum`) with variants `New`, `Analyzing`, `Fixed`, `Rejected` and derive `DeriveActiveEnum` with `sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")`.
- The enum should implement `Display` and `FromStr` or use SeaORM's attribute macros for string mapping: `#[sea_orm(string_value = "New")]` on each variant.
- Remove the `Relation` to `advisory_status` from the `advisory` entity's `RelationEnum` and `Related` impl.
- Check `entity/src/sbom_advisory.rs` for any indirect references to `advisory_status` and update if necessary.
- Follow the existing entity patterns visible in `entity/src/sbom.rs` and `entity/src/package.rs` for column definition style.
- Per docs/constraints.md §5 (Code Change Rules): inspect the existing entity code before modifying; follow patterns referenced in Implementation Notes.

## Reuse Candidates
- `entity/src/advisory.rs` — existing advisory entity with current column definitions and relation patterns to follow
- `entity/src/sbom.rs` — reference SeaORM entity demonstrating column definitions and derive macros

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines a `status` column of enum type mapped to `advisory_status_enum`
- [ ] The `AdvisoryStatusEnum` Rust enum is defined with variants New, Analyzing, Fixed, Rejected
- [ ] The `status_id` column and relation to `advisory_status` are removed from the advisory entity
- [ ] `entity/src/lib.rs` no longer registers an `advisory_status` module
- [ ] The entity crate compiles without errors: `cargo check -p entity`

## Test Requirements
- [ ] Verify `cargo check -p entity` passes with no errors
- [ ] Verify that the `AdvisoryStatusEnum` correctly maps to/from the PostgreSQL enum values

## Verification Commands
- `cargo check -p entity` — entity crate compiles cleanly

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create database migration for advisory status enum

[sdlc-workflow] Description digest: sha256-md:1fb8c5e4156e5e0b067bc7db63b92e206b53ad2cfab0ec4c015ba477d7fe09a8
