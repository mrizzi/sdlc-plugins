# Task 3: Update SeaORM entity definitions for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to reflect the new database schema after the advisory status enum migration. The `advisory` entity must replace its `status_id` integer foreign key column with a `status` column mapped to the `advisory_status_enum` PostgreSQL enum type. The `advisory_status` entity file must be removed since the lookup table no longer exists. All module re-exports in `entity/src/lib.rs` must be updated accordingly.

## Files to Modify
- `entity/src/advisory.rs` -- replace `status_id: i32` column with `status: AdvisoryStatusEnum` column using SeaORM's `DeriveActiveEnum`
- `entity/src/lib.rs` -- remove the `advisory_status` module declaration and re-export

## Files to Create
- `entity/src/advisory_status_enum.rs` -- define `AdvisoryStatusEnum` Rust enum with `DeriveActiveEnum` mapping to the PostgreSQL `advisory_status_enum` type, with variants `New`, `Analyzing`, `Fixed`, `Rejected`

## Implementation Notes
Define the enum using SeaORM's `DeriveActiveEnum` derive macro, which maps Rust enum variants to PostgreSQL enum values. The enum definition should follow this pattern:

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

In `entity/src/advisory.rs`, replace the `status_id` column definition with a `status` column of type `AdvisoryStatusEnum`. Remove any `Relation` definition that references the `advisory_status` table.

Follow the existing entity patterns in `entity/src/sbom.rs` and `entity/src/package.rs` for struct and column naming conventions.

Per CONVENTIONS.md Key Conventions: use SeaORM for database entity definitions.
Applies: task modifies `entity/src/advisory.rs` matching the convention's `.rs` entity file scope.

## Acceptance Criteria
- [ ] `AdvisoryStatusEnum` is defined with `DeriveActiveEnum` and four variants
- [ ] `entity/src/advisory.rs` uses `status: AdvisoryStatusEnum` instead of `status_id: i32`
- [ ] Relation to `advisory_status` table is removed from advisory entity
- [ ] `advisory_status` module is removed from `entity/src/lib.rs`
- [ ] Entity crate compiles without errors

## Test Requirements
- [ ] `cargo build -p entity` compiles successfully
- [ ] Enum serialization round-trips correctly (New -> "New" -> New)

## Verification Commands
- `cargo build -p entity` -- entity crate compiles without errors
- `cargo test -p entity` -- entity tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 2 -- Create database migration for advisory status enum

## additional_fields
- **labels**: ai-generated-jira, workflow:feature-branch
- **priority**: High
- **fixVersions**: RHTPA 2.0.0
