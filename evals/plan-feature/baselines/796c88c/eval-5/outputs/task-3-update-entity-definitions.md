## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema. Replace the `status_id` foreign key field in the advisory entity with a `status` enum field, define the Rust enum mapping for `advisory_status_enum`, and remove the `advisory_status` entity module entirely.

## Files to Modify
- `entity/src/advisory.rs` -- Replace `status_id: i32` foreign key field with `status: AdvisoryStatusEnum` enum field; update the SeaORM column and relation definitions
- `entity/src/lib.rs` -- Remove the `advisory_status` module re-export; add the new `AdvisoryStatusEnum` enum type (or its module)

## Files to Create
- `entity/src/advisory_status_enum.rs` -- Define the `AdvisoryStatusEnum` Rust enum with SeaORM `DeriveActiveEnum` derive macro, mapping to the PostgreSQL `advisory_status_enum` type with variants: New, Analyzing, Fixed, Rejected

## Implementation Notes
- Follow the existing entity pattern in `entity/src/advisory.rs` for column definitions and SeaORM derives
- Use SeaORM's `DeriveActiveEnum` to map the Rust enum to the PostgreSQL enum type
- Remove the `advisory_status` relation from the advisory entity since the lookup table no longer exists
- Remove `entity/src/advisory_status.rs` if it exists (the lookup table entity is no longer needed)
- Update `entity/Cargo.toml` if additional SeaORM feature flags are required for enum support

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` uses `status: AdvisoryStatusEnum` instead of `status_id: i32`
- [ ] `AdvisoryStatusEnum` enum is defined with variants New, Analyzing, Fixed, Rejected and maps to PostgreSQL `advisory_status_enum`
- [ ] The `advisory_status` entity module is removed from `entity/src/lib.rs`
- [ ] All entity definitions compile without errors

## Test Requirements
- [ ] Entity definitions compile and pass `cargo check` in the entity crate
- [ ] SeaORM enum mapping correctly serializes and deserializes all four status values

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 2 -- Database migration (enum column)
