## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new advisory schema. Replace the `status_id` foreign key field in the advisory entity with a `status` enum field using the `advisory_status_enum` PostgreSQL type. Remove the `advisory_status` entity definition entirely since the lookup table no longer exists. Update `entity/src/lib.rs` to remove the `advisory_status` module registration.

## Files to Modify
- `entity/src/advisory.rs` — replace `status_id: i32` foreign key field with `status: AdvisoryStatusEnum` enum field; remove the `Relation::AdvisoryStatus` variant and its relation definition
- `entity/src/lib.rs` — remove `pub mod advisory_status;` module declaration

## Files to Create
None — the `advisory_status.rs` file is deleted, not created.

## Implementation Notes
- In `entity/src/advisory.rs`, define a Rust enum `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected` and derive `sea_orm::EnumIter` and `sea_orm::DeriveActiveEnum` to map to the PostgreSQL `advisory_status_enum` type
- Use `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]` on the enum, and `#[sea_orm(string_value = "new")]` etc. on each variant
- Replace the `status_id` column in the `Model` struct with `status: AdvisoryStatusEnum`
- Remove the `Relation::AdvisoryStatus` variant from the `Relation` enum and its `RelationDef` implementation
- Remove the `impl Related<super::advisory_status::Entity> for Entity` block
- Follow the existing entity pattern in `entity/src/sbom.rs` for struct layout and derive macros
- The `entity/src/advisory_status.rs` file should be deleted (it defines the now-removed lookup table entity)

## Reuse Candidates
- `entity/src/sbom.rs` — demonstrates the project's SeaORM entity pattern (Model struct, Relation enum, Related impl)
- `entity/src/advisory.rs` — the existing file being modified, provides the current structure to adapt

## Acceptance Criteria
- [ ] `advisory.rs` entity uses `AdvisoryStatusEnum` enum field instead of `status_id` foreign key
- [ ] `AdvisoryStatusEnum` is defined with SeaORM derive macros mapping to `advisory_status_enum` PostgreSQL type
- [ ] `Relation::AdvisoryStatus` and its `Related` impl are removed
- [ ] `advisory_status.rs` entity file is deleted
- [ ] `lib.rs` no longer declares the `advisory_status` module
- [ ] `entity` crate compiles without errors

## Test Requirements
- [ ] `cargo build -p entity` compiles successfully
- [ ] Enum variants correctly map to PostgreSQL enum values (verified by SeaORM derive macro correctness)

## Verification Commands
- `cargo build -p entity` — entity crate builds without errors
- `cargo check --workspace` — no broken references to `advisory_status` entity across the workspace

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main


[sdlc-workflow] Description digest: sha256:3b8f9eca1600729c54294c04234795411d42af92086742efd1ce728a4f5c2cc8
