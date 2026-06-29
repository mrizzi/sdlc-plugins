## Repository
trustify-backend

## Target Branch
TC-9005

## Jira Metadata
- Priority: High
- Fix Version: RHTPA 2.0.0

## Description
Update the SeaORM entity definitions to reflect the new advisory status enum schema. The `advisory` entity must use a `status` enum field instead of the `status_id` foreign key, and the `advisory_status` entity file must be removed since the lookup table no longer exists.

## Files to Modify
- `entity/src/advisory.rs` — Replace `status_id` FK field with `status` enum field using `advisory_status_enum` type
- `entity/src/lib.rs` — Remove the `advisory_status` module registration

## Files to Create
- None

## Implementation Notes
- In `entity/src/advisory.rs`, replace the `status_id: i32` field (with its `belongs_to` relation to `advisory_status`) with a `status: AdvisoryStatusEnum` field
- Define a Rust enum `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected` that maps to the PostgreSQL `advisory_status_enum` type using SeaORM's `DeriveActiveEnum` derive macro
- The enum definition can be placed in `entity/src/advisory.rs` alongside the entity, following SeaORM conventions for inline enum definitions
- Remove the `belongs_to` relation from `Advisory` to `AdvisoryStatus` since the FK no longer exists
- In `entity/src/lib.rs`, remove the `pub mod advisory_status;` line
- Follow the existing entity pattern in `entity/src/sbom.rs` for field definitions and SeaORM derive macros
- Per CONVENTIONS.md §Framework: use SeaORM for database entity definitions. Applies: task modifies `entity/src/advisory.rs` matching the convention's Rust file scope.

## Reuse Candidates
- `entity/src/sbom.rs` — Example SeaORM entity definition with field types and derive macros; follow this pattern for the updated advisory entity

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` uses a `status: AdvisoryStatusEnum` enum field instead of `status_id` FK
- [ ] `AdvisoryStatusEnum` Rust enum is defined with variants matching the PostgreSQL enum values
- [ ] `advisory_status` entity module is removed from `entity/src/lib.rs`
- [ ] The `advisory_status.rs` entity file is deleted
- [ ] All SeaORM derive macros compile successfully

## Test Requirements
- [ ] Entity definitions compile without errors
- [ ] `AdvisoryStatusEnum` correctly maps to PostgreSQL `advisory_status_enum` type
- [ ] Removed `advisory_status` module does not cause unresolved import errors elsewhere

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Create database migration for advisory status enum

[sdlc-workflow] Description digest: sha256-md:6ad6f4eabff4a8174e50e3aeeb15f85118101e14854c4f869932233a92886ed9
