# Task 3: Update SeaORM entity definitions for advisory status enum

## Repository

trustify-backend

## Target Branch

TC-9005

## Description

Update the SeaORM entity definitions to reflect the new schema. The `advisory` entity must replace the `status_id` foreign key column with a `status` column mapped to a Rust enum. The `advisory_status` entity file should be removed since the lookup table no longer exists. All entity re-exports in `entity/src/lib.rs` must be updated accordingly.

## Acceptance Criteria

- `entity/src/advisory.rs` has a `status` field of type `AdvisoryStatusEnum` instead of `status_id: i32`
- A Rust enum `AdvisoryStatusEnum` with variants `New`, `Analyzing`, `Fixed`, `Rejected` is defined and derives `EnumIter` and `DeriveActiveEnum` for SeaORM mapping
- The entity no longer defines a relation to `advisory_status`
- `entity/src/lib.rs` no longer re-exports `advisory_status`
- The project compiles with the updated entity definitions

## Test Requirements

- Verify the `AdvisoryStatusEnum` enum can be serialized to and deserialized from the PostgreSQL enum values
- Verify that removing the `advisory_status` entity does not produce compilation errors across the workspace

## Files to Modify

- `entity/src/advisory.rs` -- replace `status_id` foreign key with `status` enum column; add `AdvisoryStatusEnum` enum definition; remove relation to `advisory_status`
- `entity/src/lib.rs` -- remove `advisory_status` module re-export

## Files to Delete

- `entity/src/advisory_status.rs` -- no longer needed; the lookup table has been dropped

## Implementation Notes

- Use SeaORM's `DeriveActiveEnum` macro to map the Rust enum to the `advisory_status_enum` PostgreSQL type
- Follow SeaORM conventions for enum mapping: `#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]`
- The enum variants should use `#[sea_orm(string_value = "New")]` etc. to match the database values exactly
- Check existing entity files like `entity/src/sbom.rs` for the pattern used for column definitions

## Dependencies

- Task 1: Create feature branch TC-9005 from main
- Task 2: Create PostgreSQL enum type and migration to add status column

[Description digest: sha256-md:c5a3f9e0d4b16a7823he0c6f9d5a4b312e8f0a6c7d9e2f3a4b5c6d7e8f9a0b12 would be posted as a comment]
