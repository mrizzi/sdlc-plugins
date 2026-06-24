## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update SeaORM entity definitions to reflect the new schema: modify the `advisory` entity to replace the `status_id` foreign key field with a `status` enum field backed by `advisory_status_enum`, define the Rust enum mapped to the PostgreSQL enum type, and remove the `advisory_status` entity module since the lookup table no longer exists.

## Files to Modify
- `entity/src/advisory.rs` — Replace the `status_id: i32` column definition with `status: AdvisoryStatusEnum` using SeaORM's `DeriveActiveEnum`; remove the `Relation` to `advisory_status`
- `entity/src/lib.rs` — Remove the `pub mod advisory_status;` re-export

## Files to Create
- `entity/src/advisory_status_enum.rs` — Define `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected` using `#[derive(DeriveActiveEnum)]` with `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]`

## Implementation Notes
- The `AdvisoryStatusEnum` must derive `DeriveActiveEnum` from SeaORM and map each variant to its PostgreSQL enum value string
- In `entity/src/advisory.rs`, change the `Model` struct: remove `pub status_id: i32` and add `pub status: AdvisoryStatusEnum`
- Remove the `Relation::AdvisoryStatus` variant from the `Relation` enum in `advisory.rs`
- Remove or delete `entity/src/advisory_status.rs` if it exists (the lookup table entity)
- Re-export `advisory_status_enum` from `entity/src/lib.rs`

Per Key Conventions (Framework): Use SeaORM's `DeriveActiveEnum` for mapping Rust enums to PostgreSQL enum types. Applies: task modifies `entity/src/advisory.rs` and creates `entity/src/advisory_status_enum.rs` matching the entity scope.

## Acceptance Criteria
- [ ] `AdvisoryStatusEnum` Rust enum exists with variants New, Analyzing, Fixed, Rejected
- [ ] `advisory.rs` entity uses `status: AdvisoryStatusEnum` instead of `status_id: i32`
- [ ] No relation to `advisory_status` table remains in entity definitions
- [ ] `entity/src/lib.rs` no longer exports `advisory_status` module
- [ ] `entity/src/lib.rs` exports the new `advisory_status_enum` module
- [ ] The crate compiles without errors

## Test Requirements
- [ ] Verify the entity crate compiles: `cargo check -p entity`
- [ ] Verify enum serialization round-trips correctly

## Verification Commands
```bash
cargo check -p entity
```

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Database migration for advisory status enum

[sdlc-workflow] Description digest: sha256-md:b2b130f3923a9cde8e5cae067972af70a6a2e70102410375dfa06c20654749f2
