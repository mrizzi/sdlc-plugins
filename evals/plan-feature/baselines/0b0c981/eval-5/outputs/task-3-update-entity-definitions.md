## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema where `advisory.status` is an enum column instead of a foreign key to the `advisory_status` lookup table. Remove the `advisory_status` entity file since the lookup table no longer exists. Update the advisory entity to define the `status` field as an enum type mapped to `advisory_status_enum`.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id` integer FK field with `status` field of type `AdvisoryStatusEnum`; add SeaORM `DeriveActiveEnum` mapping for the enum
- `entity/src/lib.rs` — remove the `advisory_status` module export

## Files to Create
- None — the enum definition should be added directly in `entity/src/advisory.rs` or a shared types module

## Implementation Notes
- In `entity/src/advisory.rs`, define an `AdvisoryStatusEnum` enum with variants `New`, `Analyzing`, `Fixed`, `Rejected` and derive `DeriveActiveEnum` with `db_type = "Enum"` and `enum_name = "advisory_status_enum"`.
- Replace the `status_id: i32` column definition with `status: AdvisoryStatusEnum` in the `Model` struct and `Column` enum.
- Remove any `Relation` definition that references the `advisory_status` entity (the FK relation to the lookup table).
- Remove the `advisory_status` module declaration from `entity/src/lib.rs`. The `entity/src/advisory_status.rs` file should be deleted as part of this task since the entity is no longer needed.
- Follow the existing entity patterns in `entity/src/sbom.rs` and `entity/src/package.rs` for struct layout and derive macros.
- Per constraints §5.1: scope changes to entity files only. Per §5.2: inspect existing entity code before modifying.

## Reuse Candidates
- `entity/src/sbom.rs` — reference for SeaORM entity struct pattern, derive macros, and column definitions
- `entity/src/package.rs` — reference for entity with enum-like fields

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected`
- [ ] `entity/src/advisory.rs` `Model` struct has `status: AdvisoryStatusEnum` field instead of `status_id: i32`
- [ ] `entity/src/advisory.rs` no longer has a relation to `advisory_status` entity
- [ ] `entity/src/advisory_status.rs` is deleted
- [ ] `entity/src/lib.rs` no longer exports the `advisory_status` module
- [ ] Entity crate compiles without errors (`cargo check -p entity`)

## Test Requirements
- [ ] `cargo check -p entity` passes with no errors
- [ ] SeaORM enum mapping correctly maps `AdvisoryStatusEnum` variants to PostgreSQL `advisory_status_enum` values

## Verification Commands
- `cargo check -p entity` — entity crate compiles cleanly

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256:5a6f61e3da690c29730de2833538856d11152ba609c7b686b538de24a01d06f4
