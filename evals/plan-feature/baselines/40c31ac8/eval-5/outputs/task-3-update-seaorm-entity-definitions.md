## Summary
Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new schema after the migration. The `advisory.rs` entity must replace the `status_id` integer foreign key column with a `status` column using the `AdvisoryStatusEnum` Rust enum. The `advisory_status` entity file must be removed since the lookup table no longer exists. The entity `lib.rs` must be updated to remove the `advisory_status` module registration.

## Files to Modify
- `entity/src/advisory.rs` -- Replace `status_id: i32` column with `status: AdvisoryStatusEnum` column; remove the relation to `advisory_status`
- `entity/src/lib.rs` -- Remove `mod advisory_status` and its re-export

## Files to Create
- `entity/src/advisory_status_enum.rs` -- Define the `AdvisoryStatusEnum` Rust enum with `DeriveActiveEnum` for SeaORM mapping to the PostgreSQL `advisory_status_enum` type

## Implementation Notes
Per CONVENTIONS.md §Module pattern: follow the existing entity module structure in `entity/src/` where each entity is a separate file registered in `lib.rs`. Applies: task modifies `entity/src/advisory.rs` and `entity/src/lib.rs` matching the convention's `.rs` module scope.

The `AdvisoryStatusEnum` should be defined with SeaORM's `DeriveActiveEnum` macro:
```rust
#[derive(Debug, Clone, PartialEq, Eq, DeriveActiveEnum)]
#[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")]
pub enum AdvisoryStatusEnum {
    #[sea_orm(string_value = "New")]
    New,
    #[sea_orm(string_value = "Analyzing")]
    Analyzing,
    #[sea_orm(string_value = "Fixed")]
    Fixed,
    #[sea_orm(string_value = "Rejected")]
    Rejected,
}
```

Reference existing entity definitions in `entity/src/sbom.rs` for the column definition pattern. Remove the `Relation::Advisory_status` variant from the advisory entity's `RelationDef` implementation.

## Acceptance Criteria
- [ ] `advisory.rs` entity uses `AdvisoryStatusEnum` column instead of `status_id` foreign key
- [ ] `advisory_status_enum.rs` defines the enum with all four values (New, Analyzing, Fixed, Rejected)
- [ ] `advisory_status` entity module is removed from `lib.rs`
- [ ] Relation to `advisory_status` table is removed from `advisory.rs`
- [ ] All entity definitions compile without errors

## Test Requirements
- [ ] Entity compilation succeeds with `cargo check -p entity`
- [ ] Enum serialization round-trips correctly (Rust enum to DB enum and back)

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 2 -- Create database migration to replace advisory_status table with enum column

## Additional Fields
- priority: High
- fixVersions: RHTPA 2.0.0
- labels: ai-generated-jira
